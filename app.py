#!/usr/bin/python

"""
lifted directly from flasktodo app -- https://github.com/gigq/flasktodo
"""
from wsgiref.handlers import CGIHandler
from wefunk_main import app

CGIHandler().run(app)
