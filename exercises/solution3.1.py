#!/usr/bin/env python3

import os, sys, re
import subprocess, shlex

from pprint import pprint

ALLOWED_COMMANDS=["shasum", "sha1sum","sha256sum", "sha512sum", "md5sum", "cat", "grep", "ls"]
NOT_ALLOWED_CHAR=["|", ">", "<", ";"]


def run( cmd, **opt ):
        result = list()
        debug = False
        if 'debug' in opt and opt['debug'] in (True, False):
            debug = opt['debug']

        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        if debug: print( "Running: '%s'" % ( " ".join( cmd ) ) )

        prc = subprocess.Popen( cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines=True )
        for line in prc.stdout.readlines():
            result.append( line )
            if prc.poll():
                break

        return (prc.returncode, result)


def command_valid( command ):

    if type( command ).__name__ == "str":
        command = shlex.split( command )

    cmdShort = re.split( r'/', command[0] )[-1]

    if cmdShort not in ALLOWED_COMMANDS:
        raise AttributeError( "Command not allowed" )

    for x in NOT_ALLOWED_CHAR:
        if x in " ".join( command ):
            raise AttributeError("Character not allowed")

    return True

if __name__ == "__main__":

    try:
        command = sys.argv[1]
        if command_valid( command ):
            pprint( run( command ) )

    except Exception as e:
        pprint(e)
