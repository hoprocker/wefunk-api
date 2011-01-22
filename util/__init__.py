import md5
from google.appengine.api import memcache

import logging

MEMCACHE_EXP = 60

def cached(func):
    func_name = func.__name__
    def cachedfunc(*args, **kwargs):
        a = list(args)
        b = list(zip(kwargs.keys(), kwargs.values()))
        a.sort()
        b.sort()
        sig = "%s%s%s" % (func_name, str(a), str(b))
        logging.debug("sig: %s" % (sig,))
        hash = md5.new(sig).hexdigest()
        data = memcache.get(hash)
        if data != None:
            return data
        data = func(*args)
        memcache.add(hash, data, MEMCACHE_EXP)
        return data
    return cachedfunc

