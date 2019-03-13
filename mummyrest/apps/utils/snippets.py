import numpy as np

from django.core.cache import cache


def get_random():
    return np.random.normal(0.5, 0.1, 1)


def get_randoms(n=1):
    return np.random.normal(0.5, 0.1, n)


def init_cache():
    cache.set('BLOK_DB', False, timeout=None)


def db_is_avaliable():
    return cache.get('BLOK_DB', False)


def blocked_db():
    return cache.set('BLOK_DB', True)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
