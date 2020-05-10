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


class DiskInfo( object ):

    def __init__( self, path, **opt ):
        self._debug = boolify( opt.get( "debug", False ) )
        self._path = path
        self._data = dict()
        self._info = dict()

    def _load( self ):
        stat = os.statvfs( self._path )

        self._data['bsize'] = stat.f_bsize
        self._data['frsize'] = stat.f_frsize
        self._data['blocks'] = stat.f_blocks
        self._data['bfree'] = stat.f_bfree
        self._data['bavail'] = stat.f_bavail
        self._info['total'] = int( self._data['frsize'] * self._data['blocks'] )
        self._info['free'] = int( self._data['frsize'] * self._data['bfree'] )
        self._info['used'] = self._info['total'] - self._info['free']

    def raw( self ):
        if len( self._data ) == 0:
            self._load()
        return self._data.copy()

    def info( self ):
        if len( self._data ) == 0:
            self._load()
        return self._info.copy()

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
        self._debug = boolify( opt.get( "debug", False ) )
        self._filename = "/etc/passwd"
        self._user = user
        self._data = dict()

    def _load( self ):
        with open( self._filename ) as fd:
            for line in fd.readlines():
                parts = re.split( ":", line.lstrip().rstrip() )
                if len( parts ) == 1: continue
                if parts[0] not in self._data:
                    self._data[ parts[0] ] = dict()
                self._data[ parts[0] ]['name'] = parts[0]
                self._data[ parts[0] ]['uid'] = parts[2]
                self._data[ parts[0] ]['gid'] = parts[3]

    def lookup( self, uid ):
        for x in self._data:
            u = self._data[x]
            if u['uid'] == uid:
                return u.copy()
        return dict()

    def exists( self ):
        if self._user not in self._data: self._load()
        if self._user in self._data:
            return True
        return False
    
    def info( self ):
        if self._user not in self._data: self._load()
        if self._user not in self._data: dict()
        return self._data[ self._user ].copy()

class Group( object ):
    def __init__( self, group, **opt ):
        self._debug = boolify( opt.get( "debug", False ) )
        self._group = group
        self._filename = "/etc/group"
        self._data = dict()

    def _load( self ):
        with open( self._filename ) as fd:
            for line in fd.readlines():
                parts = re.split( ":", line.lstrip().rstrip() )
                if len( parts ) == 1: continue
                if parts[0] not in self._data:
                    self._data[ parts[0] ] = dict()
                self._data[ parts[0] ]['name'] = parts[0]
                self._data[ parts[0] ]['gid'] = parts[2]
                self._data[ parts[0] ]['users'] = re.split( ",", parts[3] )

    def lookup( self, gid ):
        for x in self._data:
            u = self._data[x]
            if u['gid'] == gid:
                return u.copy()
        return dict()

    def exists( self ):
        if self._group not in self._data: self._load()
        if self._group in self._data:
            return True
        return False
    
    def info( self ):
        if self._group not in self._data: self._load()
        if self._group not in self._data: dict()
        return self._data[ self._group ].copy()

##############################################################################
###### Util functions
##############################################################################

def is_instamce_of( obj, ref ):
    if type( obj ).__name__ == ref:
        return True
    return False

def size_to_bytes( size ):
    pass

def apply_value(  lookup, string ):
    for key in lookup:
        string = re.sub( "{{\s*%s+\s*}}" % ( key ), lookup[ key ], string )
    return string

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
        elif test['type'] in ( "service" ): test_service( conf, test, **opt )


    return overall_res


def print_help( s ):
    print("%s <config.json>" % ( s ) )

def print_test( name, result, update = False ):
    pass

if __name__ == "__main__":
    opts = dict()
    opts['script'] = os.path.basename( sys.argv.pop(0) )
    opts['debug'] = False
    opts['lookup'] = dict()
    opts['vars'] = dict()

    try:
        opts['cfile'] = sys.argv.pop(0)
    except Exception as e:
        print_help( opts[ 'script'] )
        sys.exit(0)

    config = Configuration( opts['cfile'], **opts )
    
    if 'debug' in config.all():
        opts['debug'] = boolify( config.get('debug') )

    if opts['debug']:
        pprint( config.all() )

    if config.defined( 'sources' ):
        for x in config.get( 'sources' ):
            print("[ ] Loading source file '%s'" % ( x ) )
            s = FileSource( x )
            for u in s.data():
                opts['vars'][u] = apply_value( opts['vars'], s.get( u ) )

    pprint( User( "root" ).info() )
    pprint( Group( "wheel" ).info() )


    if run_tests(  opts['vars'] , config.get('tests'), **opts ):
        print("All is well")
    else:
        print("Some errors occured")
    