#!/usr/bin/env python3

# Json example, parsin.
# ref: https://docs.python.org/3/library/json.html

import sys, os, json, re
from pprint import pprint

## reading text file, clean read, one line at a time.
## Note that this reader is stripping all whitespaces at beginnging and end of each line!!
## All reading is meant to be used for configuration! (mainly json)
def _read_text( filename ):
    result = list()
    try:
        fd = open( filename, "r" )
        for line in fd.readlines():
            # strip all whitespaces
            result.append( line.lstrip().rstrip() )
        return result
    except Exception as e:
        print("ERROR Reading %s: %s" % ( filename, e ))

    return result

## read filename directly and parse content
def _read_json_pure( filename ):
    return json.load( open( filename ) ) )

## convert the text read from file from json (assumed) to python internal structure
def _read_json( filename ):
    return json.loads( "\n".join( _read_text( filename ) ) )

## File loading abstraction, special handling of json files
def load_file( filename ):
    filesplit = re.split( r"\.", filename )
    if filesplit[-1] in ( "json" ):
        return _read_json( filename )
    else:
        return _read_text( filename )

## Write json content, nicely formated, to file
def _write_json( filename, data ):
    return _write_text( filename, json.dumps( data, indent=2, sort_keys=True ) )

## generic file writer
def _write_text( filename, data ):
    fd = open( filename, "w" )
    fd.write( str( data ) )
    fd.close()

## File writer abstraction with special handling of json files
def write_file( filename, data ):
    filesplit = re.split( "\.", filename )
    if filesplit[-1] in ( "json" ):
        return _write_json( filename, data )
    else:
        return _write_text( filename, data )

if __name__ == "__main__":

    data = '''
    {
        "name":"test1",
        "type":"sample",
        "debug":"False",
        "tags":[
            "testing",
            "sample",
            "demo"
        ]
    }
    '''

    strct = {"name": "test1",
    "tags": ["testing", "sample", "demo"],
    "type": "sample"}

    print("\n## Json loading, printed as pprint in python format")
    print("\n#--------------------------------------")
    data_py = json.loads( data )
    pprint( data_py )
    print("\n#--------------------------------------")


    print("\n## Structure, printed as json converted from python structure format")
    print("\n#--------------------------------------")
    print( json.dumps( strct ) )
    print("\n#--------------------------------------")
    print( json.dumps( strct, sort_keys=True, indent=4, separators=(',', ': ')))
    print("\n#--------------------------------------")

    if len( sys.argv ) > 1:
        filename = sys.argv[1]
        print("\n## Json taken from file : %s" % (filename) )
        if os.path.exists( filename ):
            pprint( load_file( filename ) )
