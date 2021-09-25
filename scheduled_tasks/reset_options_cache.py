import json
from datetime import datetime


def reset_options(date_to_remove: str = str(datetime.utcnow().date())):
    """
    Remove old dates from database/yf_cached_options.json
    Parameters
    ----------
    date_to_remove : string
        Format: YYYY-MM-DD
    """
    with open(r"database/yf_cached_options.json", "r+") as r:
        data = json.load(r)
        for ticker, stats in data.items():
            for date in stats["ExpirationDate"]:
                if date == date_to_remove:
                    data[ticker]["ExpirationDate"].remove(date)
                    if date in data[ticker]["CurrentDate"]:
                        del data[ticker]["CurrentDate"][date]
        r.seek(0)
        r.truncate()
        json.dump(data, r, indent=4)


if __name__ == '__main__':
    reset_options(date_to_remove="2021-09-17")
