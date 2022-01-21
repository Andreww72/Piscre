# Piscre
Mini project implementing Raspberry Pi Zero WH with Waveshare 7.5inch (HD) screen.
Obviously done in many other places but I wanted to do it myself.
Every other repo I saw had shit all, way overcomplicated it, or no longer worked.

Steps:

0) Hardware setup (YouTube this or something), stick screen in photo frame.
1) Run installation script
2) Install other stuff I forgot
3) Get free API keys for OpenWeatherMap, CoinMarkertCap, News API, & Twitter
4) Run with "python3 drawer.py", e.g. with crontab:
0 6,8,12,16,20 *   *   *   python3 /path/to/Piscre/drawer.py
  - crontab -l
  - crontab -e
