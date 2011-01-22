from flask import Flask
app = Flask(__name__)

from flask import request

from business import ShowBusiness
from util import TestHelper
from actions import Test

@app.route("/")
def main():
    return "hi"

@app.route("/test/")
def do_test():
    ret = TestHelper.runTestsFromModule(Test)
    return ret
