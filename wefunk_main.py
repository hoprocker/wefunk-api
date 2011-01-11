from flask import Flask
app = Flask(__name__)

from flask import request
import business
from actions import Test

@app.route("/test/")
def do_test():
    show = Test.test_datastore()

    ret = "saved show: %s<br/>\n" % (show,)
    for s in business.getAllShows():
        ret += "show: %s<br/>\n" % (s.date,)
    return ret
