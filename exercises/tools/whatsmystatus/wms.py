#!/usr/bin/env python3

import os, sys, re, stat
import json
import datetime
import shlex, subprocess

from pprint import pprint

class FileSource( object ):

    def __init__( self, filename, **opt ):
        self._debug = opt.get( "debug", False )
        self._filename = filename
        self._data = dict()
    
    def _load( self ):
        pass

    def data( self ):
        return self._data.copy()

class Command( object ):

    def __init__( self, command, **opt ):
        self._debug = opt.get( "debug", False )
        self._cache_data = opt.get( "cache", False )
        self._cmd = command
        self._output = list()
        self._exitval = 0
        self._failed = False
    
    def run_r( self ):
        pass

    def run_i( self ):
        pass

    def exitval( self ):
        return self._exitval
    

class Environment( object ):
    def __init__(self):
        pass

class DiskInfo( object ):

    def __init__( self, path, **opt ):
        pass

    def info( self ):
        pass

class Config( object ):
    def __init__( self, filename, **opt ):
        self._debug = opt.get( "debug", False )
        self._filename = filename
        self._data = dict()

    def _load( self ):
        self._data = json.load( open( self._filename ) )

    def get( self, key ):
        if key not in self._data:
            raise RuntimeError( "No such config key item %s" % ( key ) )

    def set( self, key, val, overwrite=False ):
        if key in self._data and not overwrite:
            raise RuntimeError( "Key %s already exists in config, no overwrite enabled" % ( key ) )
        self._data[ key ] = val

    def all( self ):
        return self._data.copy()


class User( object ):
    def __init__( self, user, **opt ):
        pass

    def eists( self ):
        pass
    
    def info( self ):
        pass

class Group( object ):
    def __init__( self, group, **opt ):
        pass

    def eists( self ):
        pass
    
    def info( self ):
        pass

##############################################################################
###### Util functions
##############################################################################

def is_instamce_of( obj, ref ):
    if type( obj ).__name__ == ref:
        return True
    return False
    
def size_to_bytes( size ):
    pass

def apply_value( key, string ):
    pass

def dirlist( path, rx=r".*" ):
    return [ x for x in os.listdir( path ) if x not in (".", "..") and re.match( rx, x ) ]

##############################################################################
###### Test functions
##############################################################################

def test_service( conf, test, **opt ):
    pass

def test_ping( conf, test, **opt ):
    pass

def test_disk( conf, test, **opt ):
    pass

def test_memory( conf, test, **opt ):
    pass

def test_user( conf, test, **opt ):
    pass

def test_file( conf, test, **opt ):
    pass

def test_url( conf, test, **opt ):
    pass


def run_tests( conf, testlist, **opt ):
    overall_res = True
    for test in testlist:
        if 'name' not in test: raise AttributeError("Missing test name")
        if 'type' not in test: raise AttributeError("Missing test type")
        if 'test' not in test: raise AttributeError("Missing test config")


    return overall_res


def print_test( name, result, update = False ):
    pass

if __name__ == "__main__":
    opts = dict()
    opts['script'] = sys.argv.pop(0)
    opts['debug'] = False
    opts['lookup'] = dict()
    