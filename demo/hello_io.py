#!/usr/bin/env python3

import sys
import getopt
import hashlib
import re
from pprint import pprint

def _read_text( filename ):
    result = list()
    try:
        fd = open( filename, "r" )
        for line in fd.readlines():
            result.append( line )
        return result
    except Exception as e:
        print("ERROR Reading %s: %s" % ( filename, e ))

    return result

def load_file( filename ):
    filesplit = re.split( r"\.", filename )

    return _read_text( filename )


def _write_text( filename, data ):
    fd = open( filename, "w" )
    fd.write( str( data ) )
    fd.close()

def write_file( filename, data ):
    filesplit = re.split( "\.", filename )
    return _write_text( filename, data )

################################################################################
## Hashing large files
################################################################################
def file_hash( filename, chksum="sha256" ):
    BLOCKSIZE = 4096

    if chksum == "sha1":
        hasher = hashlib.sha1()
    elif chksum == "sha224":
        hasher = hashlib.sha224()
    elif chksum == "sha256":
        hasher = hashlib.sha256()
    elif chksum == "sha384":
        hasher = hashlib.sha384()
    elif chksum == "sha512":
        hasher = hashlib.sha512()
    else:
        hasher = hashlib.sha256()

    with open( filename, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()



if __name__ == "__main__":

    checksum = "sha256"
    filename = None
    if len( sys.argv ) > 1:
        filename = sys.argv[1]

    if len( sys.argv ) > 2:
        checksum = sys.argv[2]

    if filename:
        print( "File lines: %s" % ( len( load_file(filename ) ) ) )
        print( "File checksum [%s]: %s" % ( checksum, file_hash( filename, chksum=checksum ) ) )
