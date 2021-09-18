from scheduled_tasks.get_popular_tickers import *
from helpers import *

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}


def download_options(symbol_list, timestamp="", threads=True, save_max_pain=False):
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
            get_ticker_stats_threaded(symbol, symbol, timestamp)
        else:
            shared.response_dict[symbol] = get_ticker_stats(symbol=symbol, date_selected=timestamp)

    if threads:
        while len(shared.response_dict) < num_requests:
            time.sleep(0.01)

    # construct stats table from responses
    stats_table = []
    for symbol, retrieved_modules_dict in shared.response_dict.items():
        if retrieved_modules_dict is not None:
            option_chain = retrieved_modules_dict["options"]

            all_dates = list(
                map(lambda x: str(datetime.fromtimestamp(x).date()), retrieved_modules_dict["expirationDates"]))

            if option_chain:
                option_chain_stats = option_chain[0]
                option_chain_list = [[], []]
                for index, type_option in enumerate(["calls", "puts"]):
                    for i in option_chain_stats[type_option]:
                        if "volume" in i:
                            volume = i["volume"]
                        else:
                            volume = 0
                        if "openInterest" in i:
                            openInterest = i["openInterest"]
                        else:
                            openInterest = 0
                        option_chain_list[index].append([i["strike"], volume, openInterest])

                call_chain_list, call_strike = [], []
                put_chain_list, put_strike = [], []

                for oi in option_chain_list[0]:
                    call_chain_list.append(oi[-1])
                    call_strike.append(oi[0])

                for oi in option_chain_list[1]:
                    put_chain_list.append(-oi[-1])
                    put_strike.append(oi[0])

                calls_df = pd.DataFrame()
                puts_df = pd.DataFrame()
                calls_df["Strike"] = call_strike
                calls_df["OI Calls"] = call_chain_list

                puts_df["Strike"] = put_strike
                puts_df["OI Puts"] = put_chain_list

                merge_df = pd.merge(calls_df, puts_df, on="Strike", how="outer")
                merge_df.index = merge_df["Strike"]
                merge_df.dropna(inplace=True)
                if not merge_df.empty:
                    strikes = np.array(merge_df["Strike"])
                    loss_list, call_loss_list, put_loss_list = [], [], []
                    for price_at_exp in strikes:
                        net_loss, call_loss, put_loss = get_loss_at_strike(price_at_exp, merge_df)
                        loss_list.append(net_loss)
                        call_loss_list.append(call_loss)
                        put_loss_list.append(put_loss)
                    merge_df["loss"] = loss_list
                    max_pain = merge_df["loss"].idxmin()
                    print(symbol, max_pain)
                    if save_max_pain:
                        print("Saving max pain to DB")
                        db.execute("INSERT OR IGNORE INTO max_pain VALUES (?, ?, ?)", (symbol, str(datetime.utcnow().date()), max_pain))
                        conn.commit()
                else:
                    print(symbol, "MAX PAIN NOT PROCESS")
                    max_pain = "N/A"
                    call_loss_list = []
                    put_loss_list = []

                stats_list = [symbol, all_dates,
                              {str(datetime.fromtimestamp(option_chain_stats["expirationDate"]).date()):
                                   {"OptionChainCall": option_chain_list[0],
                                    "OptionChainPut": option_chain_list[1],
                                    "CallLoss":  call_loss_list,
                                    "PutLoss":  put_loss_list,
                                    "MaxPain": max_pain,
                                    "NextUpdate": str(datetime.utcnow() + timedelta(hours=1))}
                               }
                              ]

            else:
                stats_list = [symbol, all_dates, {}]
            stats_table.append(stats_list)

    # reset for future reuse
    shared.response_dict = {}

    columns = ['Symbol', 'ExpirationDate', 'CurrentDate']
    financial_data_df = pd.DataFrame(stats_table, columns=columns)
    financial_data_df.set_index('Symbol', inplace=True)
    financial_data_df = financial_data_df.to_json(orient="index").replace("\/", "/")
    financial_data_df = json.loads(financial_data_df)
    return financial_data_df


@multitasking.task
def get_ticker_stats_threaded(request_idx, symbol, timestamp):
    shared.response_dict[request_idx] = get_ticker_stats(symbol=symbol, date_selected=timestamp)


def get_ticker_stats(symbol, date_selected: str = ""):
    """
    Returns advanced stats for one ticker
    """
    if date_selected != "":
        url = 'https://query2.finance.yahoo.com/v7/finance/options/{}?date={}'.format(symbol, date_selected)
    else:
        url = 'https://query2.finance.yahoo.com/v7/finance/options/{}'.format(symbol)
    print(url)
    result = requests.get(url, headers=headers)
    json_dict = result.json()
    if json_dict['optionChain']['result'] is None or json_dict['optionChain']['result'] == []:
        return None
    module_dict = json_dict['optionChain']['result'][0]

    return module_dict


def save_options_to_json(list_of_tickers, timestamp="", save_max_pain=False):
    output = download_options(list_of_tickers, timestamp=timestamp, save_max_pain=save_max_pain)
    if output == {}:
        output = {list_of_tickers[0]: {
            "ExpirationDate": [],
            "CurrentDate": {}
        }}

    with open(r"database/yf_cached_options.json", "r+") as r:
        data = json.load(r)
        for ticker in list_of_tickers:
            if ticker in data and len(data[ticker]["ExpirationDate"]) > 4:
                data[ticker]["CurrentDate"].update(output[ticker]["CurrentDate"])
            else:
                data.update(output)
        r.seek(0)
        r.truncate()
        json.dump(data, r, indent=4)
    return output


if __name__ == '__main__':
    ticker_list = full_ticker_list()
    # save_options_to_json(list_of_tickers=["AAPL"], timestamp=1631203200)
    # snp_symbols = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"].to_list()
    # combined_symbols = list(set(snp_symbols + ticker_list))
    # save_options_to_json(list_of_tickers=combined_symbols)
    # print(combined_symbols)
    save_options_to_json(list_of_tickers=ticker_list, save_max_pain=True)
