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
    for x in range( n ):
        sleeptime = randint( 100 )
        plist[x] = multiprocessing.Process( target=simple_worker, args=(x,sleeptime))

    for i in plist:
        p = plist[i]
        p.start()

    return plist




if __name__ == "__main__":

    opt = dict()
    plist = spawn_simple_workers(10)
    for i in plist:
        p = plist[i]
        p.join()