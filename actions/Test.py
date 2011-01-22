try: 
    from django.utils import simplejson as json
except:
    import json

from datetime import datetime
from types import IntType

from google.appengine.ext import db

from business import ShowBusiness
from util import ShowScrape
from models import Show,Track


SHOW_PAGE = "test/fixtures/show_page.html"
INDEX_HTML = "test/fixtures/index_page.html"

def test_parseAndStore():
    cnt = ShowBusiness.getShowCount()
    assert type(cnt) == IntType

def _tracksort(a, b):
    if a["start_mspos"] < b["start_mspos"]: return -1
    elif a["start_mspos"] > b["start_mspos"]: return 1
    else: return 0
