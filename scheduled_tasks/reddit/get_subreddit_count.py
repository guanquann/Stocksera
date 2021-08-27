from datetime import datetime
import sqlite3
import praw

from scheduled_tasks.reddit.config import *

CLIENT_ID = API_REDDIT_CLIENT_ID
CLIENT_SECRET = API_REDDIT_CLIENT_SECRET
USER_AGENT = API_REDDIT_USER_AGENT
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

interested_subreddits = {
    "ALL": ["wallstreetbets", "stocks", "StockMarket", "options", "pennystocks", "investing", "SPACs", "Shortsqueeze"],
    "GME": ["Superstonk", "GME"],
    "AMC": ["amcstock"],
    "CLOV": ["CLOV"],
    "BB": ["BB_Stock"],
    "AMD": ["AMD_Stock"],
    "UWMC": ["UWMCShareholders"],
    "NIO": ["NIO"],
    "TSLA": ["teslainvestorsclub"],
    "AAPL": ["AAPL"],
    "NOK": ["Nokia_stock"],
    "NVDA": ["NVDA_Stock"],
    "MSFT": ["Microsoft"],
    "RBLX": ["RBLX"],
    "F": ["Fordstock"],
    "PLTR": ["PLTR"],
    "COIN": ["CoinBase"],
    "RKT": ["TeamRKT"],
    "MVIS": ["MVIS"],
    "FUBO": ["fuboinvestors"],
    "VIAC": ["VIAC"],
    "SNDL": ["SNDL_Stock"],
    "SPCE": ["SPCE"],
    "SNAP": ["SNAP"],
    "OCGN": ["Ocugen"],
    "ROKU": ["Roku"],
    "BABA": ["baba"],
    "SE": ["SE_stock"],
    "EXPR": ["EXPR"],
    "KOSS": ["KOSSstock"],
    "SOFI": ["sofistock"],
    "WKHS": ["WKHS"],
    "TLRY": ["TLRY"],
    "CLNE": ["CLNE"],
    "WISH": ["Wishstock"],
    "CLF": ["clf_Stock"],
    "GOEV": ["goev"],
    "DKNG": ["DKNG"],
    "AMZN": ["AMZN"],
    "XPEV": ["XPEV"],
    "NKLA": ["NKLA"],
    "CLVS": ["CLVSstock"],
    "BNGO": ["BNGO"],
    "SKLZ": ["SKLZ"],
    "CRSR": ["CRSR"],
    "NAKD": ["NAKDstock"],
    "ICLN": ["ICLN"],
    "PSFE": ["PSFE"],
    "XELA": ["XELAstock"],
    "SPRT": ["SPRT"],
    "MMAT": ["MMAT"],
    "HOOD": ["HOODstock"],
    "LCID": ["LCID"],
    "NVAX": ["NVAX"],
    "MRNA": ["ModernaStock"],
    "SPS": ["SOSStock"],
    "CTRM": ["CTRM"],

    "CRYPTO": ["cryptocurrency"],
    "BTC": ["Bitcoin"],
    "ETH": ["ethereum"],
    "ADA": ["cardano"],
    "BNB": ["binance"],
    "UDST": ["Tether"],
    "XRP": ["XRP"],
    "DOGE": ["dogecoin"],
    "DOT": ["Polkadot"],
    "USDC": ["USDC"],
    "SOL": ["Solana"],
    "SHIB": ["SHIBArmy"],
    "BUSD": ["binance"],
    "UNI": ["UNISwap"],
    "LINK": ["Chainlink"],
    "MATIC": ["maticnetwork"],
    "ICP": ["ICPTrader"],
    "CAKE": ["pancakeswap"],
    "CRO": ["cro"],
    "ATOM": ["cosmosnetwork"],
    "ALGO": ["algorand"],
    "XLM": ["xlm"],
    "XMR": ["xmrtrader"],
    "AAVE": ["Aave_Official"],
    "NEO": ["NEO"],
    "BCH": ["Bitcoincash"]
}
date_updated = str(datetime.now()).split()[0]


def subreddit_count():
    """
    Get number of redditors, percentage of active redditors and growth in new redditors
    """
    print("-" * 100)
    print("Getting Subreddit Stats now ...")
    for key, subreddit_names in interested_subreddits.items():
        for subreddit_name in subreddit_names:
            subreddit = reddit.subreddit(subreddit_name)
            print("Looking at {} now.".format(subreddit))
            subscribers = subreddit.subscribers
            print(subscribers)
            active = subreddit.accounts_active
            percentage_active = round((active / subscribers)*100, 2)

            db.execute("SELECT subscribers FROM subreddit_count WHERE subreddit=? ORDER BY subscribers DESC LIMIT 1",
                       (subreddit_name, ))
            try:
                prev_subscribers = db.fetchone()[0]
                growth = round((subscribers / prev_subscribers) * 100 - 100, 2)
            except TypeError:
                growth = 0

            db.execute("INSERT INTO subreddit_count VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (key, subreddit_name, subscribers, active, date_updated, percentage_active, growth))
            conn.commit()


if __name__ == '__main__':
    subreddit_count()
