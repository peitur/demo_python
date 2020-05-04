#!/usr/bin/env python3

import os, sys, re
import subprocess, shlex

from pprint import pprint

def run_ping( opt={} ):
        result = list()
        debug = False

        if 'debug' in opt and opt['debug'] in (True, False):
            debug = opt['debug']

        numStr = ""
        if 'num' in opt and opt["num"] and type( opt['num'] ).__name__ == "int":
            numStr = "-c %s" % ( opt["num"] )

        if 'host' not in opt:
            raise AttributeError("Missing host")

        cmd = "ping %s %s" % ( numStr, opt['host'] )
        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        if debug: print( "Running: '%s'" % ( " ".join( cmd ) ) )

        prc = subprocess.Popen( cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True )
        for line in prc.stdout.readlines():
            if prc.poll():
                break

        return prc.returncode


if __name__ == "__main__":

    options = dict()
    if len( sys.argv ) > 1:
        options['host'] = sys.argv[1]

    if len( sys.argv ) > 2:
        options['num'] = int( sys.argv[2] )

    rch = run_ping( options )
    if rch != 0:
        raise RuntimeError( "Ping failed to connect to %s" % ( options['host'] ) )
