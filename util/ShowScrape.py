#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import urllib
import re
try: 
    from django.utils import simplejson as json
except:
    import json
from types import FileType
from datetime import datetime,date
from business import ShowBusiness

BASE_HOST = "www.wefunkradio.com"
BASE_URL = "http://%s" % (BASE_HOST,)
INDEX_URL = "%s/shows/" % (BASE_URL,)
SHOW_URL = "%s" % (BASE_URL,)  ## append /yyyy-mo-dd

## at some point this link might change...
MP3_PATH = "http://wf.digvm.com/WeFunk_Show_%s_%s.mp3" ## show number, date in yyyy-mm-dd


"""
index page format:

<div class="show archiveshows">
  <div class="showitem montageleft">    <-- montageleft for images
    <div class="header">
      <h2><a class="nu" href="/show/yyyy-mm-dd">show name</a></h2>   <-- show link & title & number
    <div class="montage">
      <a><img src="" /></a>                    <-- image, if present
    <p class="sp">


show page format:

<head>
  <meta property="og:url" content="http://www.wefunkradio.com/show/yyyy-mm-dd">

<div id="contentflexmargin">
  <div id="hwrap">
    <h1>Show ###</h1>               <-- show number
  <div class="lofix">
    <p id="showdescription">            <-- show description
    <p id="credits">                <-- dj/donation credits
  <div id="playlistbox">
    <ul id="playlist">
      <li>
        <span class="plitem">title</span>   <-- playlist title
  <p id="shownav_bottom">
    <a class="shownav-l" href="">
    <a class="shownav-r" href="">


javascript w/ info format:

var trackextra = [[], [{"a":"artist", "t":"title"}],...];       <-- track artist/title info
var trackisfav = [0,0,0,0...];                                  <-- if track is favorited
var tracks = {"tracks":[{"approx":0,mspos:##,"ix":"aa"},...],"mstotal":##,"showdate":"yyyy-mm-dd","shownum":"###"};     <-- show info, track data
"""

def refreshShowIndex(until=0):
    """
    start by grabbing the show index page, then dig into the first show
    and navigate backwards through them (follow "shownav-r" links) until
    either there are no more or show number "until" has been reached
    """
    shows_meta = parseShowIndexPage(fetchPage(INDEX_URL))

    if len(shows_meta["shows"]) < 1:
        print "ERROR: no shows parsed"
        return -1
    
    if int(shows_meta["newest"]["number"]) < until:
        return 0

    show_url = urllib.basejoin(SHOW_URL, shows_meta["shows"][0]["href"])
    show = parseShowPage(fetchPage(show_url))

    tot = 0
    while int(show["number"]) > until:
        ##ShowBusiness.addShow(show)
        show_url = urllib.basejoin(SHOW_URL, show["prevshow_url"])
        show = parseShowPage(fetchPage(show_url))
        tot += 1

    ## we didn't touch shows so it's still valid as basis for comparison
    return tot


def parseShowIndexPage(html):
    """
    parse a show index page and return metadata
    """
    if type(html) == FileType:
        html = html.read()
    tree = BeautifulSoup(html)
## TODO : add img urls
    ret = {
            "shows":list(map(lambda(x): {
                            "name":_extractNameFromIndexNode(x),
                            "href":_extractHrefFromIndexNode(x),
                            "number":_extractShowNumFromIndexNode(x),
                            }, tree.findAll(name="div", attrs={"class":re.compile("\\bshowitem\\b")})))
            }
    ret["newest"] = max(ret["shows"], key=lambda(x): int(x["number"]))
    ret["oldest"] = min(ret["shows"], key=lambda(x): int(x["number"]))

    return ret

def parseShowPage(html):
    """
    parse show data from a page's html and return metadata
    """
    page = BeautifulSoup(html)
    
    content = page.find("div", id=re.compile("\\bcontentflexmargin\\b"))
    ret = {}
    ret["desc"] = content.find("p", id="showdescription").string
    ret["credits"] = content.find("p", id="credits").text

    tracks_meta = extractTrackJson(html)
    ret["mstotal"] = tracks_meta["tracks"]["mstotal"]
    ret["number"] = int(tracks_meta["tracks"]["shownum"])
    d = datetime.strptime(tracks_meta["tracks"]["showdate"], "%Y-%m-%d")
    ret["date"] = date(d.year, d.month, d.day)
    ret["audio_url"] = MP3_PATH % (ret["number"], ret["date"].strftime("%Y-%m-%d"))
    ret["img_url"] = 0  ## TODO, imoprt me
    ret["page_url"] = page.find("meta", attrs={"property": "og:url"})["content"]
    ret["name"] = content.find("div", id=re.compile("\\bplaylistbox\\b")).find("span", attrs={"class":re.compile("\\bplitem\\b")}).string

    ns = content.find("a", attrs={"class":re.compile("\\bshownav-l\\b")})
    if ns != None:
        ret["nextshow_url"] = ns["href"]
    else: ret["nextshow_url"] = None
    ps = content.find("a", attrs={"class":re.compile("\\bshownav-r\\b")})
    if ps != None:
        ret["prevshow_url"] = ps["href"]
    else: ret["prevshow_url"] = None

## now build the array of track info
    ret["tracks"] = []
    for i in range(0, len(tracks_meta["tracks"]["tracks"])):
        tr = {
                "start_mspos": tracks_meta["tracks"]["tracks"][i]["mspos"]
            }
        try:
            tr["artist"] = tracks_meta["tracksextra"][i][0]["a"]
        except:
            tr["artist"] = ""
        try:
            tr["title"] = tracks_meta["trackextra"][i][0]["t"]
        except:
            tr["title"] = ""

        ret["tracks"].append(tr)
    return ret

def extractTrackJson(html):
    return {
            "trackextra": json.read(re.search("var trackextra = (.*);", html).groups()[0]),
            "tracks": json.read(re.search("var tracks = (.*);", html).groups()[0]),
            "favorited": json.read(re.search("var trackisfav = (.*);", html).groups()[0]),
        }

def fetchPage(url):
    print "fetching url %s" % (url,)
    return urlopen(url).read()

def _extractShowNumFromIndexNode(node):
    return re.match("[^\\d]*(\\d+)", node.find("h2").find("a", attrs={"class":re.compile("\\bnu\\b")}).string).groups()[0]
def _extractNameFromIndexNode(node):
    return node.find("h2").find("a", attrs={"class":re.compile("\\bnu\\b")}).string
def _extractHrefFromIndexNode(node):
    return node.find("h2").find("a", attrs={"class":re.compile("\\bnu\\b")})["href"]


