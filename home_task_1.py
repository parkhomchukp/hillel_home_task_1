import pathlib
import os
import random
import time
import functools
from collections import OrderedDict, Counter
import requests
import sys
from time import sleep


def profile(msg='Elapsed time'):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            print(msg, f'({f.__name__}): {time.time() - start}s')
            return result
        return deco
    return internal


def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args):
            # Забрасываем url в список ключей
            deco._list_of_keys.append(args)
            if args in deco._cache:
                return deco._cache[args]
            result = f(*args)
            # Удаление из словаря значения, если в нем больше чем задано max_limit
            if len(deco._cache) >= max_limit:
                # Узнаем наименее часто повторяющийся ключ
                least_common_key = Counter(deco._list_of_keys).most_common()[-2][0]
                del deco._cache[least_common_key]
            deco._cache[args] = result
            return result
        deco._cache = OrderedDict()
        # Создаем список с ключами
        deco._list_of_keys = []
        return deco
    return internal


@profile(msg='Elapsed time')
@cache(max_limit=5)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://youtube.com')
fetch_url('https://youtube.com')
fetch_url('https://reddit.com')
print(fetch_url._cache)
