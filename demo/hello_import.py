#!/usr/bin/env python3
import os, sys, re
import datetime
import importlib

from pprint import pprint



def dload1( module_name, what=None ):
    mod = importlib.import_module( module_name )

    if what:
        return getattr( mod, what )
    return mod

if __name__ == "__main__":

    mname1 = "hello_url"
    mname2 = "hello_class"
    mname3 = "hello_iterator"
    i1 = dload1( mname1, "get_pypi_url" )
    i2 = dload1( mname2, "Test2" )
    i3= dload1( mname3 )

    pprint( i1("test") )
    pprint( i2.create( "test2" ).__str__() )
    for i in i3.RandomInteger( 10, 10 ):
        pprint( "> %s" % ( i ) )
