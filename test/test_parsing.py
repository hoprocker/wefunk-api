from types import DictType,ListType,IntType,StringType
from datetime import date

import util.ShowScrape as ShowScrape
from BeautifulSoup import BeautifulSoup

PAGE_HTML = "test/fixtures/show_page.html"
INDEX_HTML = "test/fixtures/index_page.html"
INDEX_SHOW_ENTRY = {
            "text":"""
<div class="showitem  montageleft">
<div class="header">
<h2><a href="/show/2004-10-01" name="20041001" title="Go to WEFUNK Show 349" class="nu">Show 349</a></h2>
<p>October 01, 2004</p>
</div>
<div class="montage"><a href="/show/2004-10-01"><img src="http://nexus.wefunkradio.com/montages/montage-show-349.jpg" height="130" width="195" alt=""></a></div><p id="sp_2004-10-01" class="sp montageleft">DJ Vadim treats us to some brand new tracks from his One Self project. (Exclusive!)</p>

</div>
""",
            "number":u"349",
            "href":u"/show/2004-10-01",
            "name":u"Show 349",
            }


def test_fetchPage():
    """
    for now just check that it actually gets a webpage.
    """
    res = ShowScrape.fetchPage(ShowScrape.BASE_URL)
    assert len(res) > 0
    assert res.find("DOCTYPE") > -1

def test_parseIndexPage():
    f = open(INDEX_HTML, "r")
    meta = ShowScrape.parseShowIndexPage(f.read())
    assert type(meta) == DictType
    assert meta.has_key("shows")
    assert meta.has_key("newest")
    assert meta.has_key("oldest")

## data integrity
    assert type(meta["shows"]) == ListType
    assert len(meta["shows"]) > 0

    for s in meta["shows"]:
        assert int(s["number"]) <= int(meta["newest"]["number"])
    for s in meta["shows"]:
        assert int(s["number"]) >= int(meta["oldest"]["number"])

## individual show attrs
    str_attrs = ("name", "href", "number")
    for show in meta["shows"]:
        for attr in str_attrs:
            assert show.has_key(attr)
            if type(show[attr]) == StringType:
                assert len(show[attr]) > 0

def test_extractShowNumFromIndexNode():
    node = BeautifulSoup(INDEX_SHOW_ENTRY["text"])
    num = ShowScrape._extractShowNumFromIndexNode(node)
    assert num == INDEX_SHOW_ENTRY["number"]
    try:
        int(num)
        works = True
    except:
        works = False
    assert works == True
def test_extractHrefFromIndexNode():
    node = BeautifulSoup(INDEX_SHOW_ENTRY["text"])
    assert ShowScrape._extractHrefFromIndexNode(node) == unicode(INDEX_SHOW_ENTRY["href"])
def test_extractNameFromIndexNode():
    node = BeautifulSoup(INDEX_SHOW_ENTRY["text"])
    assert ShowScrape._extractNameFromIndexNode(node) == unicode(INDEX_SHOW_ENTRY["name"])

def test_parseShowPage():
    f = open(PAGE_HTML, "r")
    meta = ShowScrape.parseShowPage(f.read())
    assert type(meta) == DictType

## test the structure
    attrs = (
            "number",
            "date",
            "desc",
            "tracks",
            "mstotal",
            "credits",
            "nextshow_url",
            "prevshow_url",
            "audio_url",
            "page_url",
            "img_url",
            "name",
        )
    for attr in attrs:
        assert meta.has_key(attr)

    assert len(meta["desc"]) > 0
    assert len(meta["credits"]) > 0
    assert type(meta["date"]) == type(date.today())
    assert type(meta["tracks"]) == ListType
    assert len(meta["tracks"]) > 0
    assert type(meta["number"]) == IntType
    assert type(meta["mstotal"]) == IntType

    for track in meta["tracks"]:
        assert type(track) == DictType
        assert track.has_key("start_mspos")
        assert track.has_key("artist")
        assert track.has_key("title")

def test_parseTrackJson():
    f = open(PAGE_HTML, "r+")
    meta = ShowScrape.extractTrackJson(f.read())

    assert type(meta) == DictType
    assert meta.has_key("trackextra")
    assert meta.has_key("tracks")
    assert meta.has_key("favorited")

    assert type(meta["trackextra"]) == ListType
    for i in range(1, len(meta["trackextra"])):
        assert type(meta["trackextra"][i]) == ListType
        assert len(meta["trackextra"][i]) > 0
        assert meta["trackextra"][i][0].has_key("a")
        assert meta["trackextra"][i][0].has_key("t")

    assert type(meta["tracks"]) == DictType
    assert meta["tracks"].has_key("tracks")
    assert meta["tracks"].has_key("showdate")
    assert meta["tracks"].has_key("mstotal")
    assert meta["tracks"].has_key("shownum")

    assert type(meta["tracks"]["tracks"]) == ListType
    for tr in meta["tracks"]["tracks"]:
        assert type(tr) == DictType
        assert tr.has_key("mspos")

    assert type(meta["favorited"]) == ListType
    assert len(meta["favorited"]) == len(meta["tracks"]["tracks"])


def test_refreshShowIndex():
    latest = ShowScrape.parseShowIndexPage(ShowScrape.fetchPage(ShowScrape.INDEX_URL))
    assert len(latest["shows"]) > 0
    span = 3
    until = int(latest["shows"][0]["number"]) - span

    num_shows_processed = ShowScrape.refreshShowIndex(until=until)
    assert num_shows_processed == span


