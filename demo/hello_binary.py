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

def file_n_bytes( filename, n ):
    try:
        line = ""
        with open( filename, "rb" ) as fd:
            byte = fd.read(1)
            i = 0
            while i < n:
                print( "%s " % ( str( binascii.hexlify( byte ) ) ), end="" )
                byte  = fd.read(1)
                i += 1

                if i == n:
                    print()

    except Exception as e:
        pprint( e )



if __name__ == "__main__":

    x = xorStr( "tets1tets1tets1tets1tets1tets1tets1tets1" )
    e = enc( "Hello World, this a first xor test", x )
    d = dec( e, x )

    pprint( x )
    pprint( e )
    pprint( d )

    file_n_bytes( "hello_binary.py", 10)
