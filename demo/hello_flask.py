#!/usr/bin/env python3

## https://flask.palletsprojects.com/en/1.0.x/quickstart

import os, sys, re
import datetime

from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def page_index():
    return "Welcome to solution 2.2"

@app.route('/time')
def page_time():
    return str( datetime.datetime.now() )

@app.route('/user/<username>')
def page_user( username ):
    return "Welcome %s" % ( username )

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=9999, debug=True )
