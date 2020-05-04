#!/usr/bin/env python3

import os, sys
import random
import string

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


if __name__ == "__main__":
    opt = dict()

    if len( sys.argv ) < 3:
        print("%s <blocks> <block-len>" %( sys.argv[0] ))
        sys.exit(1)

    nblocks = int( sys.argv[1] )
    blength = int( sys.argv[2] )

    print("# Blocks: %d" % ( nblocks ) )
    print("# Block length: %d" % ( blength ) )
    print("# Total length: %d" % ( nblocks * blength ) )

    if blength < 4:
        print("To short block length, must be over 4")
        exit(1)

    result = ""

    for i in range( nblocks ):
        s = ""
        while not has_number( s ) or not has_lowercase( s ) or not has_uppercase( s ) or not has_special( s ):
            s = random_string( blength )
        result += s
    print( result )
