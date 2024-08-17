import os
import sys
from io import StringIO

import requests
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from helpers import header


def ychart_data(url):
    r = requests.get(url, headers=header)
    df = pd.read_html(StringIO(r.text))
    return df
