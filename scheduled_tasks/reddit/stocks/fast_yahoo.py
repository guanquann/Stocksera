import scheduled_tasks.reddit.stocks.shared as shared
import requests
import numbers
import multitasking as multitasking
import time
import math
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}


def download_advanced_stats(symbol_list, module_name_map, threads=True):
    """
    Downloads advanced yahoo stats for many tickers by doing one request per ticker.
    """
    num_requests = len(symbol_list)
    if threads:
        num_threads = min([num_requests, multitasking.cpu_count() * 2])
        multitasking.set_max_threads(num_threads)

    # get raw responses
    for request_idx, symbol in enumerate(symbol_list):
        if threads:
            get_ticker_stats_threaded(symbol, symbol, module_name_map)
        else:
            shared.response_dict[symbol] = get_ticker_stats(symbol, module_name_map)

    if threads:
        while len(shared.response_dict) < num_requests:
            time.sleep(0.01)

    # construct stats table from responses
    stats_table = []
    for symbol, retrieved_modules_dict in shared.response_dict.items():
        stats_list = [symbol]

        for module_name, stat_name_dict in module_name_map.items():
            retrieved_module_dict = None
            if retrieved_modules_dict is not None and module_name in retrieved_modules_dict:
                retrieved_module_dict = retrieved_modules_dict[module_name]

            if retrieved_module_dict is not None:
                for stat_name in stat_name_dict.keys():
                    stat_val = 'N/A'
                    if stat_name in retrieved_module_dict:
                        stat = retrieved_module_dict[stat_name]
                        if isinstance(stat, dict):
                            if stat:  # only if non-empty otherwise N/A
                                if stat_name == "shortPercentOfFloat":
                                    stat_val = stat['fmt']
                                else:
                                    stat_val = stat['raw']
                        elif isinstance(stat, str) or isinstance(stat, numbers.Number):
                            stat_val = stat
                        else:
                            raise TypeError('Expected dictionary, string or number.')
                    stats_list.append(stat_val)
            else:
                stats_list.extend(['N/A'] * len(stat_name_dict))

        stats_table.append(stats_list)

    # reset for future reuse
    shared.response_dict = {}

    columns = ['Symbol']
    for stat_name_dict in module_name_map.values():
        columns.extend(list(stat_name_dict.values()))

    financial_data_df = pd.DataFrame(stats_table, columns=columns)
    financial_data_df.set_index('Symbol', inplace=True)

    return financial_data_df


def download_quick_stats(symbol_list, quick_stats_dict, threads=True):
    """
    Downloads select ("quick") stats for many tickers using minimal number of http requests. Splits the ticker list
    into groups of 1000 and performs one request per group. eg if list has 2350 tickers, will split into 2 groups of
    1000 tickers and one group with the remaining 350 tickers, and will get quick stats with only 3 http requests. Only
    returns those tickers that are valid, thus can be used to validate tickers efficiently.
    """
    # through trial and errors, 1179 was the max without returning an errors, but that number feels too arbitrary
    max_params = 1000
    num_requests = math.ceil(len(symbol_list)/max_params)
    last_request_size = len(symbol_list) % max_params
    if last_request_size == 0:
        last_request_size = max_params

    if threads:
        num_threads = min([num_requests, multitasking.cpu_count() * 2])
        multitasking.set_max_threads(num_threads)

    # get raw responses
    for request_idx in range(num_requests):

        if request_idx == num_requests - 1:
            num_symbols = last_request_size
        else:
            num_symbols = max_params

        request_symbol_list = symbol_list[request_idx * max_params:request_idx * max_params + num_symbols]

        if threads:
            quick_stats_request_threaded(request_idx, request_symbol_list, list(quick_stats_dict.keys()))
        else:
            shared.response_dict[request_idx] = quick_stats_request(request_symbol_list, list(quick_stats_dict.keys()))

    if threads:
        while len(shared.response_dict) < num_requests:
            time.sleep(0.01)

    # construct stats table from responses
    stats_table = []
    for response_list in shared.response_dict.values():
        # each iteration is one symbol; (eg SIGL, AAPL)
        for retrieved_stats_dict in response_list:
            symbol = retrieved_stats_dict['symbol']
            stats_list = [symbol]
            if retrieved_stats_dict is not None:
                for quick_stat_name in quick_stats_dict.keys():
                    stat_val = 'N/A'
                    if quick_stat_name in retrieved_stats_dict:
                        stat = retrieved_stats_dict[quick_stat_name]
                        if isinstance(stat, dict):
                            if stat:  # only if non-empty otherwise N/A
                                if quick_stat_name == "floatShares":
                                    stat_val = stat['fmt']
                                else:
                                    stat_val = stat['raw']
                        elif isinstance(stat, str) or isinstance(stat, numbers.Number):
                            stat_val = stat
                        else:
                            raise TypeError('Expected dictionary, string or number.')
                    stats_list.append(stat_val)
            else:
                stats_list.extend(['N/A'] * len(quick_stats_dict.keys()))

            stats_table.append(stats_list)

    # reset for future reuse
    shared.response_dict = {}

    # construct dataframe
    columns = ['Symbol'] + list(quick_stats_dict.values())
    stats_df = pd.DataFrame(stats_table, columns=columns)
    stats_df.set_index('Symbol', inplace=True)

    return stats_df


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
    if not "quoteSummary" in json_dict:
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
    if not "quoteResponse" in json_dict:
        return None
    data_list = json_dict['quoteResponse']['result']
    return data_list
