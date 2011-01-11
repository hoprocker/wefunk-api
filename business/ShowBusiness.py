from models import Show,Track


def addShow(show_info, tracks):
    """
    show = Show()
    show.number = show_info["number"]
    show.date = show_info["date"]
    show.mstotal = show_info["mstotal"]
    show.put()
    
    t_list = []
    for t in tracks:
        t_list.append(addTrack(show.key(), t).key())
    show.playlist = t_list
    show.put()

    return show
    """
    pass

def addTrack(for_show, track_info):
    track = Track()
    track.artist = track_info["artist"]
    track.title = track_info["title"]
    track.start_mspos = track_info["start_mspos"]
    track.show = for_show
    track.put()

    return track

def getAllShows(keys_only=False):
    return Show.all(keys_only=keys_only)

def getShowCount():
    return Show.all().count()
