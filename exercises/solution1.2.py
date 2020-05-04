#!/usr/bin/env python3

import os, sys
import random
import string
import datetime
import json
from flask import Flask, escape, request

app = Flask(__name__)


from pprint import pprint

SPECIAL=""

def random_string( length ):
    return ''.join( random.SystemRandom().choice( SPECIAL + string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range( length ))

def has_lowercase( block ):
    for i in string.ascii_lowercase:
        if i in block:
            return True
    return False

def has_uppercase( block ):
    for i in string.ascii_uppercase:
        if i in block:
            return True
    return False


def has_number( block ):
    for i in string.digits:
        if i in block:
            return True
    return False


def has_special( block ):
    if len( SPECIAL ) == 0:
        return True

    for i in SPECIAL:
        if i in block:
            return True
    return False

@app.route('/random')
def page_mkcode_default( ):
    return page_mkcode( 8, 4 )

@app.route('/random/<blocks>/<bsize>')
def page_mkcode( blocks, bsize ):
    result = ""
    for i in range( int( blocks ) ):
        s = ""
        while not has_number( s ) or not has_lowercase( s ) or not has_uppercase( s ) or not has_special( s ):
            s = random_string( int( bsize ) )
        result += s

    return json.dumps( {"timestamp": str( datetime.datetime.now() ), "code": result, "length": str( int( bsize ) * int( blocks ) ) } )


if __name__ == "__main__":
    app.run( host="0.0.0.0", port=9999, debug=True )
