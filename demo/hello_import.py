#!/usr/bin/env python3
import os, sys, re
import datetime
import importlib

from pprint import pprint



def dload1( module_name, what ):
    mod = importlib.import_module( module_name )
    return getattr( mod, what )

if __name__ == "__main__":

    mname1 = "hello_url"
    mname2 = "hello_class"
    i1 = dload1( mname1, "get_pypi_url" )
    i2 = dload1( mname2, "Test2" )

    pprint( i1("test") )
    pprint( i2.create( "test2" ).__str__() )
