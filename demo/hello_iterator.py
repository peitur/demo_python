#!/usr/bin/env python3

import random
import string

from pprint import pprint

## Creating two types of simple iterators/generators

# The "yield" call will do a "partial" return that can be used with iterators for continued processing.
def rand_int( n, max=100 ):
    for i in range( n ):
        yield random.randint(1, max )



## NOTE: this will breake the recusion stack!! Too many recursive calls. The calls are NOT tail recursive
def prime_numbers( n ):
    yield n
    yield from prime_numbers( n + 1 )

def prime_filter( p ):
    n = next( p )
    yield n
    yield from prime_filter( i for i in p if i % n != 0 )


## In a class, the __iter__ method can be used to do a partial iteration
class RandomInteger( object ):
    def __init__( self, n, max ):
        self._num = n
        self._maxval = max

    def __iter__( self ):
        for i in range( self._num ):
            yield random.randint(1, self._maxval )



class RandomString( object ):

    def __init__( self, len = 8 ):
        self._length = len
        self._subset = string.digits+string.ascii_lowercase+string.ascii_uppercase

    def __iter__( self ):
        res = ""
        for r in RandomInteger( self._length, self._length ):
            res += self._subset[ r ]
        yield res

if __name__ == "__main__":

    for i in rand_int( 10, 69 ):
        print( i )

    print( "# ---------------------------------- ")
    for x in RandomInteger( 10, 99 ):
        print( x )

    print( "# ---------------------------------- ")

    for i in range( 10 ):
        for t in RandomString( 32 ):
            print( "%d : %s" % ( i, t ) )

    print( "# ---------------------------------- ")

    p = 0
    g = prime_filter( prime_numbers(2) )
    while p < 1024:
        p = next( g )
        print(p)
