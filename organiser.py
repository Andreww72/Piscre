import fetcher
from read_env import read_env

read_env()
res = fetcher.get_coins()
print(res)

