try: 
    from django.utils import simplejson as json
except:
    import json

from datetime import datetime,date
from types import IntType,DictType

from google.appengine.ext import db

from business import ShowBusiness
from util import ShowScrape
from models import Show,Track

from urllib2 import urlopen


SHOW_PAGE = "test/fixtures/show_page.html"
INDEX_HTML = "test/fixtures/index_page.html"
SHOW_PAGE_UNICODE = "http://session.wefunkradio.com/show/2010-07-09"

def test_showDatastoreAccess():
    cnt = ShowBusiness.getShowCount()
    assert type(cnt) == IntType

    sh = ShowBusiness.addShow("asdf", 3, date(10, 2, 4), "asdfasdf", "asdfasfd", 10, [])
    assert ShowBusiness.getShowCount() == cnt+1
    db.delete(sh)
    assert ShowBusiness.getShowCount() == cnt

def test_scrapeAndStore():

    show_info = ShowScrape.parseShowPage(open(SHOW_PAGE,"r").read())
    assert len(show_info["tracks"]) > 0

    sh_cnt = ShowBusiness.getShowCount()
    show = ShowBusiness.addShow(**show_info)
    assert ShowBusiness.getShowCount() == sh_cnt+1
    assert ShowBusiness.getShow(show_info["number"]) != None
    assert ShowBusiness.getShowTrackCount(show_info["number"]) > 0

def test_refreshShowIndex():
    show_cnt = ShowBusiness.getShowCount()

    newnum = ShowScrape.refreshShowIndex(650)
    assert ShowBusiness.getShowCount() == newnum+show_cnt

    ## do it twice and make sure it doesn't repeat
    ShowScrape.refreshShowIndex(600)
    assert ShowBusiness.getShowCount() == newnum+show_cnt

def test_scrapeAndStoreUnicode():
    show_info = ShowScrape.parseShowPage(urlopen(SHOW_PAGE_UNICODE).read())
    
