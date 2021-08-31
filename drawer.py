import fetcher
from read_env import read_env

read_env()
#print(fetcher.get_coins())
#print(fetcher.get_news())
print(fetcher.get_wotd())
print(fetcher.get_datetime())

