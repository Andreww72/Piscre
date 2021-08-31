import os
import re
import json
import twitter
import requests
from pyowm.owm import OWM
from datetime import datetime
from typing import List, Dict, Tuple


def get_request(url, headers=None, params=None):
    """
    Perform a standard get request with optional headers and/or parammeters
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        print(e)
        return None


def get_datetime() -> Tuple[str, str]:
    """
    Return current time and day of the week
    """
    now = datetime.now().strftime('%b-%d-%I%M%p-%G')
    day = datetime.today().weekday()
    day_str = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    return (now, day_str[day],)


def get_wotd() -> Tuple[str, str]:
    """
    Return the word of the day from OED Twitter account, with Oxford dictionary definition
    """
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

    return wotd


def get_weather() -> Dict:
    owm = OWM(os.environ["openweather_key"])
    mgr = owm.weather_manager()
    canberra_lat = -35.28346
    canberra_long = 149.12807

    def fetch_weather():
        try:
            data = mgr.one_call(lat=canberra_lat, lon=canberra_long, exclude="minutely")
            return data
        except Exception as e:
            print(e)
            return None
    
    def _parse_data(weather):
        temp = weather.get_temperature(unit="celsius")
        humidity = weather.get_humidity()
        weather_code = weather.get_weather_code()
        # Get feels like as well
        return (
            weather_code,
            temp.get("min"),
            temp.get("max"),
            temp.get("temp"),
            humidity,
        )

    data = fetch_weather()
    weather = dict()

    current = data.current
    current_res = {
        "temp": current.temperature(),
        "humidity": current.humidity,
        "wind": current.wind(),
        "status": (current.status, current.detailed_status,)
    }
    weather["current"] = current_res
    
    daily = data.forecast_daily
    daily_res = list()
    for i in range(7):
        day_res = {
            "temp": daily[i].temperature(),
            "humidity": daily[i].humidity,
            "wind": daily[i].wind(),
            "status": (daily[i].status, daily[i].detailed_status,)
        }
        daily_res.append(day_res)
    weather["daily"] = daily_res
    
    hourly = data.forecast_hourly
    hourly_res = list()
    for i in range(24):
        hour_res = {
            "temp": hourly[i].temperature(),
            "humidity": hourly[i].humidity,
            "wind": hourly[i].wind(),
            "status": (hourly[i].status, hourly[i].detailed_status,)
        }
        hourly_res.append(hour_res)
    weather["hourly"] = hourly_res

    return weather


def get_weather_icon(icon, width):
    """"
    Return the icon, resized, for a given weather - works for all darksky values of "icon"
    """
    img = Image.open(os.path.join(picdir, "weather/", icon + ".png"))
    return ImageOps.invert(img.resize(width, width))


def get_news() -> Dict:
    """
    Get top Australian news headlines from newsapi.org
    """
    url = "https://newsapi.org/v2/top-headlines?country=au"
    headers = {"X-Api-Key": os.environ["news_key"]}
    return get_request(url, headers=headers)


def get_coins() -> Dict:
    """
    Return the current price of Bitcoin and Ethereum in Australian Dollars
    """
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

    return get_request(url, headers=headers, params=parameters)

