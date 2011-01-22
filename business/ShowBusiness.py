from types import IntType

from google.appengine.ext import db

from models import Show,Track


def addShow(name, number, date, page_url, audio_url, mstotal, tracks, img_url="", desc="", credits="", *args, **kwargs):
    show = Show()
    show.name = name
    show.credits = credits
    show.desc = desc
    show.number = number
    show.date = date
    show.mstotal = mstotal
    show.put()
    
    t_list = []
    for t in tracks:
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

def getAllShows(keys_only=False, get_num=50):
    return Show.all(keys_only=keys_only).order("-number").fetch(get_num)

def getShowsBefore(begin_show, get_num=50):
    try:
        begin_show = int(begin_show)
    except:
        begin_show = getLatestShowNum()
    return db.Query(Show).filter("number <= ", begin_show).fetch(get_num)

def getLatestShow():
    return db.Query(Show).order("-number").get()

def getLatestShowNum():
    return db.Query(Show).order("-number").get().number

def getShow(shownum):
    try: shownum=int(shownum)
    except: return []
    return db.Query(Show).filter('number = ', shownum).get()

def getTrack(key):
    return Track.get(key)

def getShowCount():
    return Show.all().count()

def getShowTrackCount(show_num):
    show = getShow(show_num)
    return len(show.playlist)

def getShowTracks(show):
    if type(show) == IntType:
        show = getShow(show)
    return show.playlist

def deleteShow(show):
    if type(show) == IntType:
        show = getShow(show)
    if show != None:
        show.delete()
        return "deleted"
    return "no object returned"


