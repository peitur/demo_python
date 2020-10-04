#!/usr/bin/env python3

import os, re, sys
import binascii
import string

from pprint import pprint

def xorStr( data_str ):
    return int( binascii.hexlify( data_str.encode() ),  16 )

def enc( msg, k ):
    return int( binascii.hexlify( msg.encode() ), 16 ) ^ k

def dec( msg, k ):
    b = format( msg ^ k, 'x' )
    return binascii.unhexlify( ( '0' * (len( b ) % 2 )) + b )

def printable( line, plist ):
    ret = b''
    for s in line:
        if s in (b'\n', b'\r',b'\t',b'\x0b', b'\x0c', b' '):
            ret += b'.'
        elif s in bytes( plist, 'ascii'):
            ret += s.to_bytes(2, byteorder='little')
        else:
            ret += b'.'

    return ret

def file_n_bytes( filename, n ):
    try:

        line = b""
        plist = string.ascii_letters + string.digits + string.punctuation
        print()
        with open( filename, "rb" ) as fd:
            m = 0
            i = 0
            byte = fd.read(1)
            while byte != b'':
#                print( "%s " % ( hex( ord( byte ) ) ), end="" )
                print( "%s " % ( binascii.hexlify( byte ).decode('utf-8') ), end="" )
                i += 1
                m += 1
                byte = fd.read(1)
                line += byte

                if i % n == 0:
#                    print()
                    print("\t%s" % ( printable( line, plist ).decode('utf-8') ) )
                    line = b""
#            print("\t%s" % ( printable( line ) ) )

        last_ind = (1 + len(line))  * 3
        totl_ind = n * 3
        print("%s\t%s" % ( " "*(totl_ind - last_ind), printable( line, plist ).decode('utf-8') ) )
        return m

    except Exception as e:
        raise



if __name__ == "__main__":

    x = xorStr( "tets1tets1tets1tets1tets1tets1tets1tets1" )
    e = enc( "Hello World, this a first xor test", x )
    d = dec( e, x )

    pprint( x )
    pprint( e )
    pprint( d )

    fname = sys.argv[0]
    if len( sys.argv ) > 1:
        fname = sys.argv[1]
    print("#====================== %s ===================" % ( fname ) )
    nbytes = file_n_bytes( fname, 32)
    print("#====================== %s bytes ===================" % ( nbytes ) )
