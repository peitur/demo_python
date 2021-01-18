#!/usr/bin/env python3

import os, sys, re
import multiprocessing

import time, random

from pprint import pprint

class Consumer( multiprocessing.Process ):
    def __init__( self , task_queue, result_queue ):
        multiprocessing.Process.__init__(self)
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._run = True

    def xstop( self ):
        self._run = False

    def run( self ):
        proc_name = self.name

        while self._run:
            next_task = self._task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % ( proc_name ) )
                self._task_queue.task_done()
                break

            print('%s: %s' % (proc_name, next_task))

            answer = next_task()

            self._task_queue.task_done()
            self._result_queue.put(answer)

        return


class Task( object ):
    def __init__( self, data ):
        self._data = data

    def __call__( self ):
        wtime = randint( 3 )
        time.sleep( wtime )
        return self._data.upper()

    def __str__( self ):
        return "%s -> %s" % ( self._data, self._data.upper() )





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


def run_simple( ):
    nprocs = randint( 32 )
    try:
        plist = spawn_simple_workers( nprocs )
        for i in plist:
            p = plist[i]
            p.join()
    except Exception as e:
        print("Worker crashed ... : %s " % (e) )

def run_oo_version( ):
    nprocs = randint( 3 )
    tasks = multiprocessing.JoinableQueue( )
    results = multiprocessing.Queue( )

    workers = [ Consumer( tasks, results) for i in range( nprocs ) ]

    for w in workers:
        w.start()

    print("Started workers ... sending work ...")

    tlist = ["a","b","c","d","e","f","g","h"]
    for x in tlist:
        tasks.put( Task( x ) )

    print( "sent work ... ")
    for x in workers:
        tasks.put( None )
    print("sent poison ... waiting to die")
    tasks.join()
    print("all dead ... "
    )
    jobs = len( tlist )
    while jobs:
        result = results.get()
        print('Result:', result )
        jobs -= 1

if __name__ == "__main__":

    opt = dict()
#    run_simple()

    run_oo_version()