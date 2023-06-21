import os
import sys
import requests
from time import mktime
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from helpers import config_keys


def main():
    t = datetime.now() - timedelta(minutes=10)
    unix_time = int(mktime(t.timetuple()))

    api_key = config_keys["WHALE_ALERT"]
    x = requests.get(f"https://api.whale-alert.io/v1/transactions?api_key={api_key}&"
                     f"min_value=1000000&start={unix_time}")
    for index, i in enumerate(x.json()["transactions"]):
        print(index, i["symbol"], i["amount_usd"], datetime.fromtimestamp(i["timestamp"]))


if __name__ == '__main__':
    main()
