import json
from datetime import datetime

from google.appengine.ext import db

import business

FIXTURE = "fixture.txt"

def test_datastore():
    info = json.loads(open(FIXTURE, "r").read())

    show_info = {
        "mstotal": info["mstotal"],
        "date": datetime.strptime(info["showdate"], "%Y-%m-%d").date(),
        "number" : int(info["shownum"])
    }

    tracks = []
    for i in range(0, len(info["tracks"])):
        track = {
            "start_mspos": info["tracks"][i]["mspos"]
        }
        if len(info["trackextra"][i]) > 0:
            track.update({"artist":info["trackextra"][i][0]["a"], "title":info["trackextra"][i][0]["t"]})
        else:
            track.update({"artist":"dj", "title":"intro"})
        tracks.append(track)
    tracks.sort(_tracksort)
    saved_show = business.addShow(show_info, tracks)

    return saved_show


def _tracksort(a, b):
    if a["start_mspos"] < b["start_mspos"]: return -1
    elif a["start_mspos"] > b["start_mspos"]: return 1
    else: return 0
