#!/usr/bin/env python3

import os, sys, re, stat
import json
import datetime
import shlex, subprocess

from pprint import pprint
 
FMT = {
    "header": '\033[95m',
    "info": '\033[94m',
    "ok": '\033[92m',
    "warning": '\033[93m',
    "fail": '\033[91m',
    "nc": '\x1b[0m'
}

FMT_HEADER=FMT['header']
FMT_INFO=FMT['info']
FMT_SUCCESS=FMT['ok']
FMT_FAILURE=FMT['fail']
FMT_WARNING=FMT['warning']
FMT_NC=FMT['nc']




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
        if self._exitval != 0:
            self._failed = True
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
        self._exitval = prc.returncode


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
    def __init__( self, user=None, **opt ):
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
                g = Group().lookup( parts[3] )
                self._data[ parts[0] ]['name'] = parts[0]
                self._data[ parts[0] ]['uid'] = parts[2]
                self._data[ parts[0] ]['gid'] = parts[3]
                self._data[ parts[0] ]['group'] = g

    def lookup( self, uid ):
        if len( self._data ) == 0: self._load()
        for x in self._data:
            u = self._data[x]
            if u['uid'] == str( uid ):
                return u.copy()
        return None

    def exists( self ):
        if len( self._data ) == 0: self._load()
        if self._user in self._data:
            return True
        return False
    
    def info( self ):
        if len( self._data ) == 0: self._load()
        if self._user and self._user not in self._data: return dict()
        return self._data[ self._user ].copy()

class Group( object ):
    def __init__( self, group=None, **opt ):
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
        if len( self._data ) == 0: self._load()
        for x in self._data:
            u = self._data[x]
            if u['gid'] == str( gid ):
                return u.copy()
        return None

    def exists( self ):
        if len( self._data ) == 0: self._load()
        if self._group in self._data:
            return True
        return False
    
    def info( self ):
        if len( self._data ) == 0: self._load()
        if self._group and self._group not in self._data: return dict()
        return self._data[ self._group ].copy()

##############################################################################
###### Util functions
##############################################################################
def system_type( ):
    c = Command( "uname -a")
    c.run()
    return re.split( "\s+", c.output()[0].rstrip().lstrip() )[0].lower()



def file_info( path ):
    if not os.path.exists( path ):
        return None
    info = dict()
    info['name'] = path
    info['size'] = os.stat( path ).st_size
    info['uid'] = os.stat( path ).st_uid
    info['owner'] = User().lookup( info['uid'] )['name']
    info['gid'] = os.stat( path ).st_gid
    info['group'] = Group().lookup( info['gid' ])['name']
    info['mode'] = re.split( "o", oct(stat.S_IMODE( os.stat( path ).st_mode)) )[-1]

    return info


def is_instamce_of( obj, ref ):
    if type( obj ).__name__ == ref:
        return True
    return False

def size_htob( s ):
    rx = re.compile( r"([0-9\.]+)([bkMG]*)[bB]*" )
    m = rx.match( s )
    nbytes = None

    if m:
        amount = m.group(1)
        unit = m.group(2)

        if unit == "k":
            nbytes = int( float( amount ) * 1024 )
        elif unit == "M":
            nbytes = int( float( amount ) * 1024 * 1024 )
        elif unit == "G":
            nbytes = int( float( amount ) * 1024 * 1024 * 1024 )
        else:
            if re.match( r"[0-9]+\.[0-9]+", amount ):
                raise AttributeError("Bad byte format. Got float value!")
            nbytes = int( amount )
    return int( nbytes )


def size_btoh( s ):
    units = { "": 1, "k": 1024, "M": 1024 * 1024, "G": 1024 * 1024 * 1024  }

    x = int( s )
    for i in units:
        c = float( x / units[i] )
        if c < 500:
            return "%s%s" % ( c, i )
    return x

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
    results = list()
    debug = boolify( test.get('debug', opt.get( "debug", False ) ) )
    w_exists = "active"
    if 'name' not in test: raise AttributeError("Missing service name")
    if 'state' in test and test['state'] in ( "exists", "present", "active" ): w_exists = "active"
    if 'state' in test and test['state'] in ( "missing", "absent", "inactive" ): w_exists = "inactive"
    if 'state' in test and test['state'] in ( "unknown", "missing" ): w_exists = "unknown"
        
    cmd = "systemctl is-active %s" % ( test['name'] )
    c = Command( cmd )
    c.run()

    if c.output()[0].rstrip().lstrip() != w_exists:
        results.append( False )

    if False in results:
        return False
    return True

def test_ping( conf, test, **opt ):
    debug = boolify( test.get('debug', opt.get( "debug", False ) ) )
    if 'host' not in test: raise AttributeError("Missing host")
    pings = int( test.get( 'pings', 1 ))
    timeout = ""
    if 'timeout' in test:
        if system_type() == "darwin":
            timeout = "-t %s" % ( test['timeout'] )
        elif system_type() == "linux":
            timeout = "-W %s" % ( test['timeout'] )
        else:
            raise AttributeError("Unsupported platform")

    command = "ping %s -c %s %s" % ( timeout, pings, apply_value( conf, test['host'] ) )
    if debug:
        print("DEBUG: Command: %s" % ( command ) )
    c = Command( command, debug=debug )
    c.run_r()

    if debug:
        print( "="*64 )
        pprint( c.output() )
        print( "="*64 )


    if c.exitval() != 0:
        return False
    return True
    
def test_disk( conf, test, **opt ):
    pass

def test_memory( conf, test, **opt ):
    pass

def test_user( conf, test, **opt ):
    results = list()
    debug = boolify( test.get('debug', opt.get( "debug", False ) ) )
    w_uid = None
    w_exists = True
    w_group = None
    if 'name' not in test: raise AttributeError("Missing username")
    if 'state' in test and test['state'] in ( "exists", "present" ): w_exists = True
    if 'state' in test and test['state'] in ( "missing", "absent" ): w_exists = False
    if 'uid' in test: w_uid = int( test['uid'] )
    if 'group' in test: w_group = test['group']

    u = User( test['name'] )
    d = u.info()
    if w_uid and w_uid != d['uid']: results.append( False )
    if w_group and w_group != d['group']['name']: results.append( False )
    if w_exists and not u.exists(): results.append( False )

    if False in results:
        return False
    return True


def test_group( conf, test, **opt ):
    results = list()
    debug = boolify( test.get('debug', opt.get( "debug", False ) ) )
    w_gid = None
    w_exists = True
    w_gid = None
    w_user = None
    if 'name' not in test: raise AttributeError("Missing username")
    if 'state' in test and test['state'] in ( "exists", "present" ): w_exists = True
    if 'state' in test and test['state'] in ( "missing", "absent" ): w_exists = False
    if 'gid' in test: w_gid = test['gid']

    u = Group( test['name'] )
    d = u.info()
    if w_exists and not u.exists(): results.append( False )
    if w_gid and w_gid != d['gid']: results.append( False )
    if w_user and w_user not in d['users']: results.append( False )

    if False in results:
        return False
    return True


def test_file( conf, test, **opt ):
    debug = boolify( test.get('debug', opt.get( "debug", False ) ) )
    if 'path' not in test: raise AttributeError("Missing path")
    if 'state' not in test: raise AttributeError("Missing state")

    results = list()
    path = test['path']
    w_exists = True
    w_mode = None
    w_owner = None
    w_group = None


    if test['state'] in ( "exists", "present" ): w_exists = True
    if test['state'] in ( "missing", "absent" ): w_exists = False
    if "mode" in test: w_mode =  apply_value( conf, test['mode'] )
    if "owner" in test: w_owner = apply_value( conf, test['owner'] )
    if "group" in test: w_group = apply_value( conf, test['group'] )

    if os.path.exists( path ):
        info = file_info( path )        

        if w_mode and w_mode != info['mode']: results.append( False )
        if w_owner and w_owner != info['owner']: results.append( False )
        if w_group and w_group != info['group']: results.append( False )

        if not w_exists: results.append( False )
        
    else:
        if w_exists: results.append( False )

    if False in results:
        return False        
    return True


def test_url( conf, test, **opt ):
    pass


def test_exec( conf, test, **opt ):
    if test['type'] in ( "ping" ): return test_ping( conf, test['test'], **opt )
    elif test['type'] in ( "service" ): return test_service( conf, test['test'], **opt )
    elif test['type'] in ( "disk" ): return test_disk( conf, test['test'], **opt )
    elif test['type'] in ( "file" ): return test_file( conf , test['test'], **opt )
    elif test['type'] in ( "user" ): return test_user( conf , test['test'], **opt )
    elif test['type'] in ( "group" ): return test_group( conf , test['test'], **opt )
    else:
        AttributeError("Unknown test type %s" % ( test['type']) )


def run_tests( conf, testlist, **opt ):
    overall_res = True
    for test in testlist:
        if 'name' not in test: raise AttributeError("Missing test name")
        if 'type' not in test: raise AttributeError("Missing test type")
        if 'test' not in test: raise AttributeError("Missing test config")

        print("[+] %sRunning test%s '%s' [%s] ... " % (  FMT_INFO, FMT_NC ,test['name'], test['type']  ), end="" )
        if test_exec( conf, test, **opt ):
            print("%sOK%s" % ( FMT_SUCCESS, FMT_NC ) )
        else:
            print("%sFail%s" % ( FMT_FAILURE, FMT_NC ) )
            overall_res = False

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
            print("[+] %sLoading source file%s '%s'" % ( FMT_HEADER, FMT_NC, x ) )
            s = FileSource( x )
            for u in s.data():
                opts['vars'][u] = apply_value( opts['vars'], s.get( u ) )

    if run_tests(  opts['vars'] , config.get('tests'), **opts ):
        print("[ ] %sAll is well%s" % (FMT_SUCCESS, FMT_NC ) )
    else:
        print("[!] %sSome errors occured%s" % ( FMT_FAILURE, FMT_NC ) )
    