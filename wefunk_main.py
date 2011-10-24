from flask import Flask,make_response
app = Flask(__name__)

from flask import request

from business import ShowBusiness
from util import TestHelper,ShowScrape
from actions import Test
from adapters import JsonAdapter

@app.route("/test/")
def do_test():
    ret = TestHelper.runTestsFromModule(Test)
    return ret

## TESTING {{{
@app.route('/showindex/')
def getIndex():
    return str(ShowScrape.getShowsList())
    return "done"

@app.route('/shows/<int:show>/tracks/')
def get_tracks_for_show(show):
    return ",".join(ShowBusiness.getShowTracks(show))


## TESTING }}}

@app.route('/shows/<int:tot>/<int:from_show>/')
@app.route('/shows/<int:tot>/')
@app.route('/shows/')
def get_shows_as_json(tot=None, from_show=None):
    shows_json = JsonAdapter.getShowsAsJson(tot, from_show)
    resp = make_response(str(shows_json))
    resp.mimetype = "application/json"
    return resp

@app.route('/admin/update/')
def update_shows():
    tot = ShowScrape.refreshShowIndex(600)
    return "%s shows updated" % (tot,)

@app.route('/admin/delete/<int:shownum>/')
def del_show(shownum):
    return ShowBusiness.deleteShow(shownum)

@app.route("/")
def dull():
    return ""

