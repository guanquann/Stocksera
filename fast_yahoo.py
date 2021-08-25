import scheduled_tasks.reddit.get_reddit_trending_stocks.shared as shared
import requests
import numbers
import multitasking as multitasking
import time
import json
import pandas as pd
from datetime import datetime, timedelta

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}

config = {'summaryDetail': ['regularMarketOpen', 'previousClose', 'dayHigh', 'fiftyTwoWeekHigh', 'regularMarketDayLow',
                            'fiftyTwoWeekLow', 'regularMarketVolume', 'averageDailyVolume10Day', 'fiftyDayAverage',
                            'twoHundredDayAverage', 'trailingPE', 'forwardPE', 'marketCap', 'beta',
                            'trailingAnnualDividendYield', 'trailingAnnualDividendRate', 'totalAssets', 'navPrice'],
          'defaultKeyStatistics': ['sharesOutstanding', 'floatShares', 'shortRatio', 'shortPercentOfFloat',
                                   'trailingEps', 'pegRatio', 'enterpriseToRevenue', 'netIncomeToCommon',
                                   'threeYearAverageReturn', 'fiveYearAverageReturn'],
          'summaryProfile': ['industry', 'sector', 'website', 'longBusinessSummary'],
          'price': ['longName', 'symbol', 'regularMarketPrice', 'quoteType', 'marketState',
                    'regularMarketChangePercent', 'regularMarketChange',
                    'postMarketChangePercent', 'postMarketChange', 'preMarketChangePercent', 'preMarketChange']}


def download_advanced_stats(symbol_list, threads=True):
    """
    Downloads advanced yahoo stats for many tickers by doing one request per ticker.
    """
    print(symbol_list, "!!!!!!!!!!!!")
    num_requests = len(symbol_list)
    if threads:
        num_threads = min([num_requests, multitasking.cpu_count() * 2])
        multitasking.set_max_threads(num_threads)

    # get raw responses
    for request_idx, symbol in enumerate(symbol_list):
        if threads:
            get_ticker_stats_threaded(symbol, symbol, config)
        else:
            shared.response_dict[symbol] = get_ticker_stats(symbol, config)

    if threads:
        while len(shared.response_dict) < num_requests:
            time.sleep(0.01)

    # construct stats table from responses
    stats_table = []
    for symbol, retrieved_modules_dict in shared.response_dict.items():

        stats_list = [symbol]

        for module_name, stat_name_dict in config.items():
            retrieved_module_dict = None
            if retrieved_modules_dict is not None and module_name in retrieved_modules_dict:
                retrieved_module_dict = retrieved_modules_dict[module_name]

            if retrieved_module_dict is not None:
                for stat_name in stat_name_dict:
                    stat_val = 'N/A'
                    if stat_name in retrieved_module_dict:
                        stat = retrieved_module_dict[stat_name]
                        if isinstance(stat, dict):
                            if stat:  # only if non-empty otherwise N/A
                                stat_val = stat['fmt']
                        elif isinstance(stat, str) or isinstance(stat, numbers.Number):
                            stat_val = stat
                        # else:
                        #     raise TypeError('Expected dictionary, string or number.')
                    stats_list.append(stat_val)
            else:
                stats_list.extend(['N/A'] * len(stat_name_dict))

        stats_table.append(stats_list)

    # reset for future reuse
    shared.response_dict = {}

    columns = ['Symbol']
    for stat_name_dict in config.values():
        columns.extend(stat_name_dict)

    financial_data_df = pd.DataFrame(stats_table, columns=columns)
    financial_data_df["next_update"] = str(datetime.utcnow() + timedelta(seconds=600))
    financial_data_df.set_index('Symbol', inplace=True)
    financial_data_df = financial_data_df.to_json(orient="index").replace("\/", "/")
    financial_data_df = json.loads(financial_data_df)
    return financial_data_df


@multitasking.task
def get_ticker_stats_threaded(request_idx, symbol, module_name_map):
    shared.response_dict[request_idx] = get_ticker_stats(symbol, module_name_map)


def get_ticker_stats(symbol, module_name_map):
    """
    Returns advanced stats for one ticker
    """

    url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/' + symbol
    module_list = list(module_name_map.keys())
    params = {
        'modules': ','.join(module_list),
    }
    result = requests.get(url, params=params, headers=headers)
    if result.status_code != 200 and result.status_code != 404:
        result.raise_for_status()

    json_dict = result.json()
    if "quoteSummary" not in json_dict:
        return None
    if json_dict['quoteSummary']['result'] is None:
        return None
    module_dict = json_dict['quoteSummary']['result'][0]

    return module_dict


@multitasking.task
def quick_stats_request_threaded(request_idx, request_symbol_list, field_list):
    shared.response_dict[request_idx] = quick_stats_request(request_symbol_list, field_list)


def quick_stats_request(request_symbol_list, field_list):
    """
    Returns quick stats for up to 1000 tickers in one request. Only returns those tickers that are valid, thus can be
    used to validate tickers efficiently.
    """
    params = {
        'formatted': 'True',
        'symbols': ','.join(request_symbol_list),
        'fields': ','.join(field_list),
    }
    result = requests.get("https://query1.finance.yahoo.com/v7/finance/quote", params=params, headers=headers)
    if result.status_code != 200 and result.status_code != 404:
        result.raise_for_status()

    json_dict = result.json()
    if "quoteResponse" not in json_dict:
        return None
    data_list = json_dict['quoteResponse']['result']
    return data_list
