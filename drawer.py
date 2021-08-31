#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import fetcher
from read_env import read_env
from waveshare_epd import epd7in5_HD
from PIL import Image,ImageDraw,ImageFont


picdir = "pic"
read_env()


# Collect data
weather = fetcher.get_weather()
crypto = fetcher.get_coins()
news = fetcher.get_news()
wotd = fetcher.get_wotd()
time, day = fetcher.get_datetime()

print(weather)
print()
print(crypto)
print()
print(news)
print()
print(wotd)
print()
print(time, day)
exit()

try:
    epd = epd7in5_HD.EPD()
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Drawing on the Horizontal image
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

    

    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'hello world', font=font24, fill=0)
    draw.text((10, 20), '7.5inch e-Paper', font=font24, fill=0)
    draw.line((20, 50, 70, 100), fill=0)
    draw.line((70, 50, 20, 100), fill=0)
    draw.rectangle((20, 50, 70, 100), outline=0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    Himage = Image.open(os.path.join(picdir, '7in5_HD.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("4.read bmp file on window")
    Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    logging.info("Goto Sleep...")
    epd.sleep()
    
except KeyboardInterrupt:    
    epd7in5_HD.epdconfig.module_exit()
    exit()
