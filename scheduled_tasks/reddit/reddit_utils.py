import re
import praw
import math
import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import scheduled_tasks.reddit.config as cfg
from helpers import *
from custom_extensions.custom_words import new_words
from custom_extensions.stopwords import stopwords_list

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

reddit = praw.Reddit(client_id=cfg.API_REDDIT_CLIENT_ID,
                     client_secret=cfg.API_REDDIT_CLIENT_SECRET,
                     user_agent=cfg.API_REDDIT_USER_AGENT)

conn = sqlite3.connect(r"database/database.db", check_same_thread=False)
db = conn.cursor()

pattern = "(?<=\$)?\\b[A-Z]{1,5}\\b(?:\.[A-Z]{1,2})?"


def round_time(time_string, base=5):
    """
    Round time to the nearest base so that minute hand on time will look nicer in db
    Parameters
    ----------
    time_string: str
        minute hand you wish to round: 08 -> 05
    base: int
        round to the nearest base
    """
    rounded = str(base * round(int(time_string)/base))
    if len(rounded) == 1:
        rounded = "0" + rounded
    return rounded


def words_to_remove():
    basic_stopwords_list = list(map(lambda x: re.sub(r'\W+', '', x.upper()), stopwords.words('english'))) + \
                           ["THATS", "GOT", "IM", "LIKE", "STILL", "EVER", "EVEN", "CANT", "US", "THATS", "GO", "WOULD",
                            "MUCH", "GET", "ONE", "SEE", "WAY", "NEED", "TAKE", "MAKE", "GETTING", "GOING", "GONNA",
                            "NEED", "THINK", "SAY", "SAID", "KNOW", "WAY", "TIME", "WEEK", "WELL", "WANT", "THING",
                            "LETS", "IVE", "COULD", "ALWAYS", "FEEL", "FELT", "FEELS", "WHATS", "REALLY", "LOOK",
                            "GUYS", "PEOPLE", "ALREADY", "IMGEMOTET_TH", "BANBET", "VISUALMOD", "TODAY", "LOOKS",
                            "MADE", "YESTERDAY", "TOMORROW", "TMR", "EDT", "KEEP", "ANYONE", "GOES", "PLEASE", "BET",
                            "BAN", "AROUND", "ANYONE", "ACTUALLY", "SEEN", "ALSO", "RIGHT", "THERES", "MAY", "MIGHT",
                            "DAY", "MAKING"]
    return basic_stopwords_list


def insert_into_word_cloud_dict(text, all_words_dict):
    """
    Extract all words from comment and insert into word cloud dict
    Parameters
    ----------
    text: str
        comment
    all_words_dict: dict
        previous dict of word cloud
    """
    for word in text.upper().split():
        word = re.sub(r'\d|\W+', '', word)
        if len(word) <= 25:
            all_words_dict[word] = all_words_dict.get(word, 0) + 1
    return all_words_dict


def get_mapping_stocks():
    mapping_stocks = {
        'TSLA': {'TESLA'},
        'GME': {'GAMESTOP'},
        'BB': {'BLACKBERRY'},
        'FB': {'FACEBOOK'},
        'OCGN': {'OCUGEN'},
        'MRNA': {'MODERNA'},
        'NVAX': {'NOVAVAX'},
        'BNTX': {'BIONTECH'},
        'NVDA': {'NVIDIA'},
        'HOOD': {'ROBINHOOD'},
        'AAPL': {'APPLE'},
        'COIN': {'COINBASE'},
        'AMZN': {'AMAZON'},
        'PYPL': {'PAYPAL'},
        'SQ': {'SQUARE'},
        'RBLX': {'ROBLOX'},
        'PLTR': {'PALANTIR'},
        'SKLZ': {'SKILLZ'},
        'MSFT': {'MICROSOFT'},
        'LCID': {'LUCID'},
        'RIVN': {'RIVIAN'},
        'GOOG': {'GOOGLE', 'ALPHABET'},
        'UPST': {'UPSTART'},
        'CLOV': {'CLOVER'},
        'TLRY': {'TILRAY'},
        'SNDL': {'SUNDIAL'},
        'TWTR': {'TWITTER'},
        'DIS': {'DISNEY'},
        'TIGR': {'TIGR'},
        'FUTU': {'MOOMOO'},
        'ZM': {'ZOOM'},
        'SPCE': {'GALACTIC'},
        'PTON': {'PELOTON'},
        'MVIS': {'MICROVISION'},
        'BA': {'BOEING'},
        'WKHS': {'WORKHORSE'},
        'NKLA': {'NIKOLA'},
        'KO': {'COKE', 'COCACOLA'},
        'SNOW': {'SNOWFLAKE'},
        'AI': {'C3.AI', 'C3AI'},
        'NET': {'CLOUDFLARE'},
        'NFLX': {'NETFLIX'},
        'MU': {'MICRON'},
        'VIAC': {'VIACOM'},
        'SHOP': {'SHOPIFT'},
        'NOK': {'NOKIA'},
        'SDC': {'SMILEDIRECTCLUB'},
        'GOEV': {'CANOO'},
        'CRSP': {'CRISPR'},
        'CRSR': {'CORSAIR'},
        'NKE': {'NIKE'},
        'SAVA': {'CASSAVA'},
        'PINS': {'PINTEREST'},
        'SBUX': {'STARBUCKS'},
        'BNGO': {'BIONANO'},
        'SENS': {'SENSEONICS'},
        'INTC': {'INTEL'},
        'F': {'FORD'},
        'EXPR': {'EXPRESS'},
        'RIDE': {'LORDSTOWN'},
        'CHWY': {'CHEWY'},
        'XLNX': {'XILINX'},
        'MSTR': {'MICROSTRATEGY'},
        'GS': {'GOLDMAN'},
        'CSCO': {'CISCO'},
        'WMT': {'WALMART'},
        'U': {'UNITY'},
        'BABA': {'ALIBABA'},
        'CRWD': {'CROWDSTRIKE'},
        'COST': {'COSTCO'},
        'V': {'VISA'},
        'SE': {'SEA'},
        'T': {'AT&T'},
        'C': {'CITIGROUP', 'CITI', 'CITIBANK'},
        'PEP': {'PEPSI'},
        'ADBE': {'ADBE'},
        'Z': {'ZILLOW'},
        'TWLO': {'TWILIO'},
        'WOOF': {'PETCO'},
        'MDB': {'MONGO', 'MONGODB'},
        'DKNG': {'DRAFTKINGS'},
        'CLF': {'CLEVELAND'},
        'BIDU': {'BAIDU'},
    }
    return mapping_stocks


def coinbase_coins():
    # List of crypto symbols interest in
    # We use symbols from coinbase instead as it is more concise than CoinGeckoAPI, which list ALL symbols (>1000)
    r = requests.get('https://api.pro.coinbase.com/currencies')
    # https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false
    crypto_dict = {}
    for coin in r.json():
        if coin['details']['type'] == 'crypto':
            crypto_dict[coin['id']] = {coin['id'].upper(), coin['name'].upper()}

    # Remove unwanted symbols
    del crypto_dict['KEEP']
    del crypto_dict['QUICK']
    return crypto_dict


def get_mapping_coins():
    # in case of duplicate key in dicts
    # latest dict overwrites previous dicts
    mapping_coins = {
        'ETH': {'ETH', 'ETHEREUM'},
        'XRP': {'XRP', 'RIPPLE'},
        'NEO': {'NEO'},
        'CEL': {'CEL', 'CELSIUS'},
        'XMR': {'MONERO', 'XMR'},
        'BNB': {'BNB', 'BINANCE COIN'},
        'NEM': {'XEM', 'NEM'},
        'TRON': {'TRX', 'TRON'},
        'BTG': {'GOLD', 'BTG'},
        'EOS': {'EOS', 'EOSIO'},
        'VET': {'VET', 'VECHAIN'},
        'DAI': {'DAI', 'MAKERDAO'},
        'SHIB': {'SHIBA', 'SHIB', 'SHIBA INU'},
        'IOTA': {'IOTA', 'MIOTA'},
        'LTO': {'LTO NETWORK', 'LTO'},
        'THETA': {'THETA'},
        'KSM': {'KUSAMA', 'KSM'},
        'CAKE': {'PANCAKESWAP', 'PANCAKE', 'CAKE'},
        'KLAY': {'KLAYTN', 'KLAY'},
        'ERG': {'ERG', 'ERGO'},
        'SAFEMOON': {'SAFEMOON'},
        'ONE': {'ONE', 'HARMONY'},
        'LUNA': {'TERRA', 'LUNA'},
        'FTM': {'FTM', 'FANTOM'},
        'XTZ': {'XTZ', 'TEZOS'},
        'ZIL': {'ZIL', 'ZILLIQA'},
        'HYVE': {'HYVE'},
        'BLOK': {'BLOK', 'BLOKTOPIA'},
        'FTT': {'FTT'},
        'CRO': {'CRO'},
        'XEC': {'XEC'},
        'BTT': {'BTT'},
        'NEXO': {'NEXO'},
        'MINA': {'MINA'},
        'SCRT': {'SCRT'},
        'CKB': {'CKB'},
    }
    return {**coinbase_coins(), **mapping_coins}
