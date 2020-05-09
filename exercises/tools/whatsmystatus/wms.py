#!/usr/bin/env python3

import os, sys, re, stat
import json
import datetime
import shlex, subprocess

from pprint import pprint

class FileSource( object ):

    def __init__( self, filename, **opt ):
        self._debug = boolify( opt.get( "debug", False ) )
        self._filename = filename
        self._data = dict()
    
    def _load( self ):
        fd = open( self._filename, "r" )
        for line in fd.readlines():
            if re.match( r"\s*#.*", line ):
                continue
            parts = re.split( r"=", line.rstrip().lstrip() )
            k = parts.pop(0).lower()
            v = "=".join( parts )

            self._data[ k ] = v

    def data( self ):
        if len( self._data ) == 0:
            self._load()

        return self._data.copy()

class Command( object ):

    def __init__( self, command, **opt ):
        self._debug = boolify( opt.get( "debug", False ) )
        self._cache_data = opt.get( "cache", False )
        self._cmd = command
        self._output = list()
        self._exitval = 0
        self._failed = False
    
    def run_r( self ):
        if is_instamce_of( self._cmd, "str" ):
            self._cmd = shlex.split( self._cmd )

        if self._debug: print( "Running: '%s'" % ( " ".join( self._cmd ) ) )

        prc = subprocess.Popen( self._cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True )
        for line in prc.stdout.readlines():
            self._output.append( line )
            if prc.poll():
                break

        self._exitval = prc.returncode
        return self._output

    def run_i( self ):
        if is_instamce_of( self._cmd, "str" ):
            self._cmd = shlex.split( self._cmd )

        if self._debug: print( "Running: '%s'" % ( " ".join( self._cmd ) ) )

        prc = subprocess.Popen( self._cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True )  
        for line in prc.stdout.readlines():

            if self._cache_data:
                self._output.append( line )

            yield line.rstrip()
            if prc.poll():
                break


    def exitval( self ):
        return self._exitval
    
    def output( self ):
        return self._output


class Environment( object ):
    def __init__(self):
        pass

class DiskInfo( object ):

    def __init__( self, path, **opt ):
        pass

    def info( self ):
        pass

class Configuration( object ):
    def __init__( self, filename, **opt ):
        self._debug = boolify( opt.get( "debug", False ) )
        self._filename = filename
        self._data = dict()

    def _load( self ):
        self._data = json.load( open( self._filename ) )

    def get( self, key ):
        if len( self._data ) == 0:
            self._load()
        if key not in self._data:
            raise RuntimeError( "No such config key item %s" % ( key ) )
        return self._data[ key ]


    def set( self, key, val, overwrite=False ):
        if len( self._data ) == 0:
            self._load()
        if key in self._data and not overwrite:
            raise RuntimeError( "Key %s already exists in config, no overwrite enabled" % ( key ) )
        self._data[ key ] = val

    def defined( self, key ):
        if key not in self._data:
            return False
        return True

    def all( self ):
        if len( self._data ) == 0:
            self._load()
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

def apply_value(  lookup, key, string ):
    if key not in lookup:
        raise AttributeError("Undefined key %s in lookup source" % ( key ) )
    return re.sub( "{{\s*\S+\s*}}", lookup[key], string )

def dirlist( path, rx=r".*" ):
    return [ x for x in os.listdir( path ) if x not in (".", "..") and re.match( rx, x ) ]

def perc_of( size, prc ):
    size = int( size )
    prc = int( prc )
    return float( size * float( prc / 100 ) )

def boolify( string ):
    if string in (True, "True", "true", "yes" ):
        return True
    elif string in (False, "False", "false", "no" ):
        return False
    else:
        raise AttributeError("Not supported boolean value %s" % ( string ))
    
def dmerge( a, b ):
    if not is_instamce_of( a, "dict" ): raise AttributeError("Merge first attribute must be doct")
    if not is_instamce_of( b, "dict" ): raise AttributeError("Merge second attribute must be doct")

    for r in b:
        a[r] = b[r]
    return a


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

        print("[+] Running test '%s' [%s] ... %-64s" % ( test['name'], test['type'], "" ) )
        if test['type'] in ( "ping" ): test_ping( conf, test, **opt )
        elif test['type'] in ( "service" ): test_service( conf, test, **opt )
        elif test['type'] in ( "disk" ): test_disk( conf, test, **opt )


    return overall_res


def print_test( name, result, update = False ):
    pass

if __name__ == "__main__":
    opts = dict()
    opts['script'] = sys.argv.pop(0)
    opts['debug'] = False
    opts['lookup'] = dict()
    opts['cfile'] = sys.argv.pop(0)
    
    external = dict()
    config = Configuration( opts['cfile'], **opts )
    
    if 'debug' in config.all():
        opts['debug'] = boolify( config.get('debug') )

    if opts['debug']:
        pprint( config.all() )

    if config.defined( 'sources' ):
        for s in config.get( 'sources' ):
            print("[ ] Loading source file '%s'" % ( s ) )
            s = FileSource( s )
            external = dmerge( external, s.data() )

    for u in external:
        external[ u ] = apply_value( external, u, external[ u ] ) 
    pprint( external )

    if run_tests( external, config.get('tests'), **opts ):
        print("All is well")
    else:
        print("Some errors occured")
    