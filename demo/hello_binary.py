#!/usr/bin/env python3

import os, re, sys
import binascii

from pprint import pprint

def xorStr( data_str ):
    return int( binascii.hexlify( data_str.encode() ),  16 )

def enc( msg, k ):
    return int( binascii.hexlify( msg.encode() ), 16 ) ^ k

def dec( msg, k ):
    b = format( msg ^ k, 'x' )
    return binascii.unhexlify( ( '0' * (len( b ) % 2 )) + b )

if __name__ == "__main__":

    x = xorStr( "tets1tets1tets1tets1tets1tets1tets1tets1" )
    e = enc( "Hello World, this a first xor test", x )
    d = dec( e, x )

    pprint( x )
    pprint( e )
    pprint( d )
