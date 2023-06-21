import os
import sys
import requests
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from helpers import header


def ychart_data(url):
    r = requests.get(url, headers=header)
    df = pd.read_html(r.text)
    return df
