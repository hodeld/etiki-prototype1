'''
Created on 26.8.2019

@author: daim
'''

from django.core.cache import cache  # default cache in locmem


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



