#!/usr/bin/env python3

import importlib

from pprint import pprint

class DynamicClass( object ):

    def __init__( self, mname, cname=None, **opt ):
        self.__debug = opt.get("debug", False )
        self.__module_name = mname
        self.__class_name = cname
        self.__module = importlib.import_module( mname )
        self.__class = None

        if cname:
            self.__class = getattr( self.__module, cname )

    def get_class( self, cls=None ):
        if cls:
            return getattr( self.__module, cls )
        return self.__class

    def get_module( self ):
        return self.__module

if __name__ == "__main__":
    o = DynamicClass( "pathlib", "Path" )
    
    p = o.get_module()
    print( p.Path( __file__ ).name )

    c = o.get_class()
    print( c( __file__ ).name )
