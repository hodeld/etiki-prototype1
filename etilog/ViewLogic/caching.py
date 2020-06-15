'''
Created on 26.8.2019

@author: daim
'''

from django.core.cache import caches
from threading import Thread

cache = caches['database']  # fastest cache on heroku so far (locmem does not work)


def postpone(function):
    """postpone -> connection needs to be closed in function if db connection"""
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


# not at postpone as sometimes not ready
def set_cache(name, value, request, timeout=3600):
    key_name = str(request.user.id) + name
    cache.set(key_name, value, timeout)


def get_cache(name, request=None):
    if request:
        key_name = str(request.user.id) + name
    else:
        key_name = name
    value = cache.get(key_name, None)
    return value


