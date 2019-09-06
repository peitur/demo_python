#!/usr/bin/env python3

from pprint import pprint

if __name__ == "__main__":

    ## empty dictionary, empty
    dict0 = dict()

    ## creting a simple dict of numbers
    dict1 = { "103":"aaaa", "101":"bbbb", "108":"cccc", "114":"dddd", "105":"eeee" }

    ## reference copy of dict1
    dict2 = dict1

    ## copying the dict into a new dict (copy, not reference)
    dict3 = dict1.copy()

    dict4 = {"a":"1111","b":"2222","c":"3333","d":"4444","e":"5555","f":"6666","g":"7777","h":"8888","i":"9999","j":"9090","k":"1010","l":"2020"}

    print("\n# start dict")
    pprint( dict1 )

    ## dict comprehension,
    print("\n# dict comprehension")
    pprint( { int( dict4[ x ] ) for x in dict4 } )

    ## map funciton, takes a transform (map) function and a dict (or iterable) object

    ## Since we copied dict1 to dict2, it's not just a reference.
    print( "\n# dict2, created as reference")
    pprint( dict2 )

    print("\n# dict3, copy of dict1")
    pprint( dict3 )

    pritn("\n# check for elemnt in dict")
    if "a" in dict4:
        print("a is in dict4")

    print("\n# lets print a dict with indexes" )
    for i, e in enumerate( dict1 ):
        print("%d > %s => %s" % ( i, e, dict1[ e ] ) )


    print("\n## Joining dicts")
    print( ", ".join( dict4.keys() ) )

    print( dict4["b"] )
    print( dict4.get("x", "missing" )
    dict4["4"] = "newval"
    dict4["x"] = "exists"
    print( dict4.get("x", "missing" )
