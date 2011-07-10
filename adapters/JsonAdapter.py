try: 
    from django.utils import simplejson as json
except:
    import json


from business import ShowBusiness
from util import cached
from types import IntType,LongType

HARD_LIMIT = 25

def getShowsAsJson(tot=HARD_LIMIT, from_show=None):
    try: tot=int(tot)
    except: tot = HARD_LIMIT
    try: from_show = int(from_show)
    except: from_show = ShowBusiness.getLatestShowNum()

    shows = ShowBusiness.getShowsBefore(from_show, min(tot, HARD_LIMIT))
    return map(ShowBusiness.showToObj, shows)

def getShowTracksAsJson(from_show):
    if from_show in [IntType,LongType]:
        from_show = ShowBusiness.getShow(from_show)
    tracks = map(lambda x: {'artist':x['artist'], 
                            'title':x['title'],
                            'start_mspos':x['start_mspos']
                            }, ShowBusiness.getShowTracks(from_show))
    return json.dumps(tracks)


