try: 
    from django.utils import simplejson as json
except:
    import json

from google.appengine.api.datastore_types import Key as key_type
from google.appengine.ext.db import ReferenceProperty as RefProp

from business import ShowBusiness
from util import cached

HARD_LIMIT = 25

def getShowsAsJson(tot=HARD_LIMIT, from_show=None):
    try: tot=int(tot)
    except: tot = HARD_LIMIT
    try: from_show = int(from_show)
    except: from_show = ShowBusiness.getLatestShowNum()

    shows = ShowBusiness.getShowsBefore(from_show, min(tot, HARD_LIMIT))
    return map(showToObj, shows)

@cached
def showToObj(show):
    obj = {}
    for p in show.properties():
        obj[p] = getattr(show, p)
    obj['playlist'] = map(lambda(x): trackToObj(ShowBusiness.getTrack(x)), obj['playlist'])
    return obj

@cached
def trackToObj(track):
    obj = {}
    for p in filter(lambda(x): type(getattr(track,x)) not in [key_type, RefProp], track.properties()):
        obj[p] = getattr(track, p)
    return obj



