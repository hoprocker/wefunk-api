from types import IntType

from google.appengine.ext import db
from google.appengine.api.datastore_types import Key as key_type
from google.appengine.ext.db import ReferenceProperty as RefProp

from models import Show,Track
from util import cached


def addShow(*args, **kwargs):
    def txn(name, number, date, page_url, audio_url, mstotal, tracks, img_url="", desc="", credits="", *args, **kwargs):
        show = Show()
        show.name = name
        show.credits = credits
        show.desc = desc
        show.number = number
        show.date = date
        show.mstotal = mstotal
        show.audio_url = audio_url
        show.img_url = img_url
        show.put()
        
        return show
    
    show = db.run_in_transaction(txn, *args, **kwargs)

    t_list = []
## FOR NOW, TODO : assuming 'tracks' is in kwargs, a **BAD** idea long-term
    if kwargs.has_key('tracks'):
        for t in kwargs['tracks']:
            t_list.append(addTrack(show.key(), t,).key())
        for i in range(0, len(t_list)-1):
            prev = (None, t_list[i-1])[i > 0]
            next = (None, t_list[i+1])[i < (len(t_list)-1)]
            updateTrackLinks(t_list[i], prev, next)
        show.playlist = t_list
        show.put()

    return show

def addTrack(for_show, track_info):
    track = Track()
    track.artist = track_info["artist"]
    track.title = track_info["title"]
    track.start_mspos = track_info["start_mspos"]
    track.show = for_show
    track.put()

    return track

def updateTrackLinks(track_key, prev, next):
    track = getTrack(track_key)
    track.next_track = next
    track.prev_track = prev
    track.put()

@cached
def getAllShows(keys_only=False, get_num=50):
    return Show.all(keys_only=keys_only).order("-number").fetch(get_num)

@cached
def getShowsBefore(begin_show, get_num=50):
    try:
        begin_show = int(begin_show)
    except:
        begin_show = getLatestShowNum()
    return db.Query(Show).filter("number <= ", begin_show).fetch(get_num)

@cached
def getLatestShow():
    return db.Query(Show).order("-number").get()

@cached
def getLatestShowNum():
    latest_show =  getLatestShow()
    if latest_show != None:
        return latest_show.number
    return 0

@cached
def getShow(shownum):
    try: shownum=int(shownum)
    except: return []
    return db.Query(Show).filter('number = ', shownum).get()

@cached
def getTrack(key):
    return Track.get(key)

@cached
def getShowCount():
    return Show.all().count()

@cached
def getShowTrackCount(show_num):
    show = getShow(show_num)
    return len(show.playlist)

@cached
def getShowTracks(show):
    if type(show) == IntType:
        show = getShow(show)
    return [trackToObj(getTrack(t)) for t in show.playlist]

def deleteShow(show):
    if type(show) == IntType:
        show = getShow(show)
    if show != None:
        show.delete()
        return "deleted"
    return "no object returned"

def clearAllShows():
    prev_cnt = getShowCount()
    [deleteShow(s) for s in getAllShows(get_num=getShowCount())]
    return prev_cnt - getShowCount()

@cached
def showToObj(show):
    obj = {}
    for p in show.properties():
        obj[p] = getattr(show, p)
    obj['playlist'] = map(lambda(x): trackToObj(getTrack(x)), obj['playlist'])
    return obj

@cached
def trackToObj(track):
    obj = {}
    for p in filter(lambda(x): type(getattr(track,x)) not in [key_type, RefProp], track.properties()):
        obj[p] = getattr(track, p)
    return obj


