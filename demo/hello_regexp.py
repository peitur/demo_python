#!/usr/bin/env python3

import sys, re, os
from pprint import pprint

if __name__ == "__main__":

    data1 = ["abcd21", "bcdeaa", "cdefa4", "defh44", "21wjekfwk"]

    pprint( data1 )

    r1 = re.compile( r'[a-z]+([0-9]+)' )
    for item in data1:
        if r1.match( item ):
            print( item )

    for item in data1:
        g = r1.findall( item )
        if g:
            pprint( g )
