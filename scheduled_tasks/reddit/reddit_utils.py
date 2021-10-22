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


def coinbase_coins():
    # List of crypto symbols interest in
    # We use symbols from coinbase instead as it is more concise than CoinGeckoAPI, which list ALL symbols (>1000)
    r = requests.get('https://api.pro.coinbase.com/currencies')
    crypto_dict = {}
    for coin in r.json():
        if coin['details']['type'] == 'crypto':
            crypto_dict[coin['id']] = {coin['id'].upper(), coin['name'].upper()}

    # Remove unwanted symbols
    # del crypto_dict['KEEP']
    # del crypto_dict['RLY']
    # del crypto_dict['FORTH']
    # del crypto_dict['FARM']
    # del crypto_dict['MASK']
    # del crypto_dict['OMG']
    return crypto_dict


def get_topics():
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
        'ERG': {'ERG', 'ERGO'}
    }
    return {**coinbase_coins(), **mapping_coins}
