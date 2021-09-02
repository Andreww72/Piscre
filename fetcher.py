import os
import re
import json
import twitter
import requests
from pyowm.owm import OWM
from datetime import datetime
from typing import List, Dict, Tuple


def get_request(url, headers=None, params=None):
    """Standard get request with optional headers and parammeters"""
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        print(e)
        return None


def day_from_num(day_num: int) -> str:
    """Day of week from number"""
    
    day_str = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    return day_str[day_num]


def get_datetime() -> Tuple[str, str]:
    """Return current time and day of the week"""

    now = datetime.now().strftime("%b-%d-%I%M%p-%G")
    day_num = datetime.today().weekday()
    return (now, day_num)


def get_wotd() -> Tuple[str, str]:
    """Word of the day from OED Twitter"""
    
    # Get OED word of the day from Twitter
    # https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/introduction
    twit = twitter.Api(
        consumer_key=os.environ["twitter_consumer_key"],
        consumer_secret=os.environ["twitter_consumer_secret"],
        access_token_key=os.environ["twitter_access_token"],
        access_token_secret=os.environ["twitter_access_token_secret"]
    )

    tweets = twit.GetUserTimeline(screen_name="OED", count=5, exclude_replies=True)

    # Extract word, try each tweet until success (sometimes tweets aren't WOTD)
    predicate = "OED Word of the Day:"
    for tweet in tweets:
        if predicate in tweet.text:
            wotd = tweet.text.split(":")[1].strip()
            wotd = wotd.split("http")[0]
    
    # Remove potential ... unicode ellipse character
    encoded = wotd.encode("ascii", "ignore")
    wotd = encoded.decode()
    return wotd


def get_weather() -> Dict:
    """Get current weather and forecast"""

    owm = OWM(os.environ["openweather_key"])
    mgr = owm.weather_manager()
    canberra_lat = -35.28346
    canberra_long = 149.12807

    try:
        data = mgr.one_call(lat=canberra_lat, lon=canberra_long, exclude="minutely")
    except Exception as e:
        print(e)
        return None
    
    weather = dict()

    current = data.current
    current_res = {
        "temp": current.temperature(),
        "humidity": current.humidity,
        "wind": current.wind()["speed"],
        "status": (current.status, current.detailed_status,)
    }
    weather["current"] = current_res
    
    daily = data.forecast_daily
    daily_res = list()
    for i in range(7):
        day_res = {
            "temp": daily[i].temperature(),
            "humidity": daily[i].humidity,
            "wind": daily[i].wind()["speed"],
            "status": (daily[i].status, daily[i].detailed_status,)
        }
        daily_res.append(day_res)
    weather["daily"] = daily_res
    
    hourly = data.forecast_hourly
    hourly_res = list()
    for i in range(12):
        hour_res = {
            "temp": hourly[i].temperature(),
            "humidity": hourly[i].humidity,
            "wind": hourly[i].wind()["speed"],
            "status": (hourly[i].status, hourly[i].detailed_status,)
        }
        hourly_res.append(hour_res)
    weather["hourly"] = hourly_res

    return weather


def get_weather_icon(status, time) -> str:
    """"Return the icon path for given status"""
    
    day_night = "night"
    status = status.lower()

    if 6 < time < 18:
        day_night = "day"
    
    if "clear" in status:
        return f"clear-{day_night}.png"
    elif "cloudy" in status:
        return f"partly-cloudy-{day_night}.png"
    elif "rain" in status:
        return "rain.png"
    elif "snow" in status:
        return "snow.png"
    elif "sleet" in status:
        return "sleet.png"
    elif "fog" in status:
        return "fog.png"
    else:
        return f"clear-{day_night}.png"


def get_news() -> Dict:
    """Top Australian news headlines from newsapi.org"""
    
    url = "https://newsapi.org/v2/top-headlines?sources=abc-news-au,australian-financial-review"
    headers = {"X-Api-Key": os.environ["news_key"]}
    data = get_request(url, headers=headers)
    titles = []
    for i in range(4):
        titles.append(data["articles"][i]["title"].split("-")[0].strip())
    return titles


def get_coins() -> Dict:
    """Current info for Bitcoin and Ethereum in AUD"""

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

    data = get_request(url, headers=headers, params=parameters)
    coins = {}
    for ticker, coin in data["data"].items():
        aud_data = coin["quote"]["AUD"]
        coins[ticker] = {
            "price": aud_data["price"],
            "volume": aud_data["volume_24h"],
            "market_cap": aud_data["market_cap"],
            "percent_24h": aud_data["percent_change_24h"],
            "percent_30d": aud_data["percent_change_30d"]
        }
    return coins

