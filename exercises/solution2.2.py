#!/usr/bin/env python3

import os, sys, re
import json
import datetime
import socket

from pprint import pprint
from flask import Flask, escape, request


def load_health( filename ):
    f = open( filename, "r")
    return json.load( f )

def status_color( health ):
    s = sum( [ float(x) for x in health['cpu'] ] )
    l = int( len( health['cpu'] ) )
    if l > 0:
        a = float( float(s)/l )
    else:
        a = 0.0

    if a < 1.0: return "green"
    if a < 2.0: return "orange"
    if a > 2.0: return "red"

    return "gray"

app = Flask(__name__)

@app.route('/')
def page_index():
    return "Welcome to solution 2.2"

@app.route('/health')
def page_heath():
    data = dict()

    data['timestamp'] = str( datetime.datetime.now() )
    data['hostname'] = socket.gethostname()
    h = load_health( "sample/health1.json" )
    data['message'] = h
    data['status'] = status_color( h )

    return json.dumps( data )

if __name__ == "__main__":
    opt = dict()
    data = dict()

    app.run( host="0.0.0.0", port=9999, debug=True )
