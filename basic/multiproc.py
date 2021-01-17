#!/usr/bin/env python3

import os, sys, re
import multiprocessing

import time, random

from pprint import pprint

def randint( rng = 10 ):
    return random.randrange( rng )


def simple_worker( i, t ):
    print("[+] Worker %d started, working %d" % ( i, t ) )
    time.sleep( t )
    print("[-] Worker %d done" % ( i ) )

def spawn_simple_workers( n ):
    plist = dict()
    print("[ ] Starting %d workers ... " % ( n ) )
    for x in range( n ):
        sleeptime = randint( 15 )
        plist[x] = multiprocessing.Process( target=simple_worker, args=(x,sleeptime))

    for i in plist:
        p = plist[i]
        p.start()

    return plist




if __name__ == "__main__":

    opt = dict()
    nprocs = randint( 32 )
    try:
        plist = spawn_simple_workers( nprocs )
        for i in plist:
            p = plist[i]
            p.join()
    except Exception as e:
        print("Worker crashed ... : %s " % (e) )