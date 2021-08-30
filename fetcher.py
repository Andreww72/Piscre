import os
import json
import twitter
import requests
import weather as w
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


def get_datetime() -> str:
    """
    Return current time and day of the week
    """
    now = datetime.now().strftime('%b-%d-%I%M%p-%G')
    day = datetime.today().weekday()
    day_str = {
        0: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
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

    statuses = twit.GetUserTimeline(screen_name="OED", count=2, exclude_replies=True)
    print(statuses)

    # Extract word
    predicate = "OED Word of the Day:"
    #tweet = data.find(tweet => {
    #  return tweet.text.indexOf(predicate) === 0
    #})
    # wotd = tweet.text.match(/^(.*)$/m)[0].replace(predicate, '').trim().split(', ')[0].trim()

    # Get root then definition of the word from Oxford Dictionaries
    # https://developer.oxforddictionaries.com/documentation
    headers = {"app_id": app_id, "app_key": app_key}
    lemmas_url = f"https://od-api.oxforddictionaries.com/api/v2/lemmas/EN-GB/{wotd.lower()}"
    root = get_request(lemmas_url, headers=headers)

    dict_url = f"https://od-api.oxforddictionaries.com/api/v2/entries/EN-GB/{root.lower()}"
    defined = get_request(dict_url, headers=headers)

    return (wotd, defined,)


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

