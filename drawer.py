#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import fetcher
from read_env import read_env
from PIL import Image, ImageDraw, ImageFont
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from waveshare_epd import epd7in5_HD


KELVIN = -273.15
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
weatherdir = os.path.join(picdir, "weather")
read_env(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))

# Collect data
weather = fetcher.get_weather()
crypto = fetcher.get_coins()
news = fetcher.get_news()
wotd = fetcher.get_wotd()
dt_res, day_num = fetcher.get_datetime()
day = fetcher.day_from_num(day_num)

try:
    # Setup screen
    epd = epd7in5_HD.EPD()
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Create image
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame 
    draw = ImageDraw.Draw(Himage)

    # Day and time
    dt = dt_res.split("-")
    draw.text((10, 0), f"{day} {dt[1]} {dt[0]} {dt[3]} @ {dt[2]}", font=font24, fill=0)
    draw.line((0, 30, 880, 30), fill=0)
    
    # News titles
    count, limit = 0, 4
    for item in news:
        # I do not want sports scores or live crap
        if count >= limit:
            break
        if "score" in item.lower():
            continue
        draw.text((10, 40+count*35), item, font=font24, fill=0)
        draw.text((10, 55+count*35), "."*220, font=font18, fill=0)
        count += 1
    
    draw.line((0, 190, 880, 190), fill=0)

    # Word of the day with def
    draw.text((10, 200), wotd, font=font24, fill=0)
    draw.line((0, 240, 880, 240), fill=0)

    # Crypto
    btc = Image.open(os.path.join(picdir, "btc.png"))
    eth = Image.open(os.path.join(picdir, "eth.png"))
    btc = btc.resize((32, 32))
    eth = eth.resize((32, 32))
    Himage.paste(btc, (10, 250))
    Himage.paste(eth, (10, 290))
    btc_price = "{:,}".format(round(crypto["BTC"]["price"]))
    btc_mcap = "{:,}".format(round(crypto["BTC"]["volume"]))
    eth_price = "{:,}".format(round(crypto["ETH"]["price"]))
    eth_mcap = "{:,}".format(round(crypto["ETH"]["volume"]))
    btc_text = f"${btc_price} w {btc_mcap} for {round(crypto['BTC']['percent_24h'], 1)}% and {round(crypto['BTC']['percent_30d'], 1)}%"
    eth_text = f"${eth_price} w {eth_mcap} for {round(crypto['ETH']['percent_24h'], 1)}% and {round(crypto['ETH']['percent_30d'], 1)}%"
    draw.text((50, 255), btc_text, font=font24, fill=0)
    draw.text((50, 290), eth_text, font=font24, fill=0)
    
    # Weather and forecast
    current = weather["current"]
    w_icon = Image.open(os.path.join(weatherdir, fetcher.get_weather_icon(current['status'][0], int(dt[2][0:2]))))
    w_icon = w_icon.resize((64, 64))
    Himage.paste(w_icon, (10, 340))
    draw.text((80, 340), f"Canberra is {current['status'][0]} at {round(current['temp']['temp'] + KELVIN, 1)}'", font=font24, fill=0)
    draw.text((80, 365), f"Feels {round(current['temp']['feels_like'] + KELVIN, 1)}' with {current['humidity']}% & {round(current['wind'], 1)}km/h", font=font24, fill=0)
    
    daily = weather["daily"]
    for i, wday in enumerate(daily):
        day_txt = fetcher.day_from_num((day_num+i) % 7)
        draw.rectangle((10+i*123, 420, 10+(i+1)*123, 520), fill=255, outline="black")
        draw.text((15+i*123, 430), f"{day_txt[0:3]}: {round(wday['temp']['min'] + KELVIN)}-{round(wday['temp']['max'] + KELVIN)}", font=font24, fill=0)
        w_icon = Image.open(os.path.join(weatherdir, fetcher.get_weather_icon(wday['status'][0], 12)))
        w_icon = w_icon.resize((48, 48))
        Himage.paste(w_icon, (40+i*125, 460))

    epd.display(epd.getbuffer(Himage))
    epd.sleep()
    
except KeyboardInterrupt:    
    epd7in5_HD.epdconfig.module_exit()
    exit()
