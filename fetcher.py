import os
import time
import json
import requests
import weather as w
from typing import List, Dict

def get_time() -> str:
    return time.time()


def get_day() -> str:
    return "Monday"


def get_weather() -> Dict:
    return {}

def get_news() -> Dict:
    return {}


def get_coins() -> Dict:
    # https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": "BTC,ETH",
        "convert": "AUD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.environ["coinmarketcap_key"],
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        print(e)
        return None

