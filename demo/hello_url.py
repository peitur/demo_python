#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html

import sys,re,os,re, datetime
import urllib.request
import json

from pprint import pprint

def get_token( ):
    return os.getenv( "GITHUB_TOKEN" )

def get_pypi_url( module = "" ):
    return "https://pypi.python.org/pypi/%s/json" % ( module )

def get_github_commit_url( user, repo ):
    return "https://api.github.com/repos/%s/%s/commits" % ( user, repo )

def get_request( url , **opt ):

    req = urllib.request.Request( url = url )
    data = None
    with urllib.request.urlopen(req) as f:
        if f.status != 200:
            raise RuntimeError("Could not load url : %s, got %s" % ( modurl, f.status ))
        data = f.read().decode('utf-8')
        return json.loads( data )

    return None

if __name__ == "__main__":
    modurl = get_pypi_url( "ipaddress" )
    json_data = get_request( modurl )

    pprint( json_data.keys() )
    pprint( sorted( json_data['releases'] ) )
    pprint( json_data["releases"]["1.0.22"] )
