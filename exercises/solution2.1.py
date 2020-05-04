#!/usr/bin/env python3

import os, sys, re
from pprint import pprint

def iterfile( filename ):
    f = open( filename, "r" )
    for line in f.readlines():
        line = line.rstrip().lstrip()
        if len( line ) > 0:
            yield line
    f.close()

if __name__ == "__main__":
    opt = dict()
    data = dict()

    if len( sys.argv ) < 2:
        print("%s <filname>" %( sys.argv[0] ))
        sys.exit(1)

    filename = sys.argv[1]

    for line in iterfile( filename ):
        for i in re.split( "\s+", line ):
            if i not in data:
                data[i] = 0
            data[i] += 1

    for i in sorted( data.items(), key=lambda x: x[1] ):
        print( i )
