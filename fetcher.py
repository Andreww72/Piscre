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


def get_weather_icon(icon, width):
    """"
    Return the icon, resized, for a given weather - works for all darksky values of "icon"
    """
    img = Image.open(os.path.join(picdir, "weather/", icon + ".png"))
    return ImageOps.invert(img.resize(width, width))


def get_news() -> Dict:
    """Get top Australian news headlines from newsapi.org"""
    url = "https://newsapi.org/v2/top-headlines?country=au"
    headers = {"X-Api-Key": os.environ["news_key"]}
    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return data
    except (requests. ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        print(e)
        return None


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

    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)
        return data
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        print(e)
        return None

