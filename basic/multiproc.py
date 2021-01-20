#!/usr/bin/env python3

import os, sys, re
import multiprocessing

import time, random

from pprint import pprint

## REF: https://pymotw.com/2/multiprocessing/communication.html

## ----------------------------------------------------------
## Events
## ----------------------------------------------------------


## ----------------------------------------------------------
## Pool
## ----------------------------------------------------------


## ----------------------------------------------------------
## Shared namespaces
## ----------------------------------------------------------


## ----------------------------------------------------------
## Shared states
## ----------------------------------------------------------


## ----------------------------------------------------------
## Syncronizing
## ----------------------------------------------------------


## ----------------------------------------------------------
## Resources
## ----------------------------------------------------------



## ----------------------------------------------------------
## Simple MapReduce
## ----------------------------------------------------------

class Generator( multiprocessing.Process ):
    
    def __init__( self, samples, nworkers, s, e, result_queue, **opts ):
        multiprocessing.Process.__init__(self)
        self._debug = opts.get("debug", False)
        self._samples = samples
        self._num_workers = nworkers
        self._int_start = s
        self._int_end = e
        self._result_queue = result_queue
        self._run = True
        print("[+] Created generator %d - %d with %d samples" % ( self._int_start, self._int_end, self._samples ) )

    def run( self ):
        proc_name = self.name
        print("[+] %s Starting generator execution %s - %s with %s samples" % ( proc_name, self._int_start, self._int_end, self._samples ) )
        
        for i in range( self._samples ):
            self._result_queue.put( randint( self._int_end ) )
        
        for i in range( self._num_workers ):
            print("Sending term %s" % ( i ) )
            self._result_queue.put( None )

        return

class Mapper( multiprocessing.Process ):

    def __init__( self, task_queue, result_queue, **opts ):
        multiprocessing.Process.__init__(self)
        self._debug = opts.get("debug", False)
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._run = True

    def run( self ):
        proc_name = self.name
        while self._run:
            data = self._task_queue.get()
            if data is None:
                print("### DONE ####")
                self._run = False

            print( "%s: %s" % ( proc_name, data ) )
            self._task_queue.task_done()    

        return

class Reducer( multiprocessing.Process ):

    def __init__( self, task_queue, result_queue, **opts ):
        multiprocessing.Process.__init__(self)
        self._debug = opts.get("debug", False)
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._run = True

    def run( self ):
        proc_name = self.name

        while self._run:
            pass

class Manager( multiprocessing.Process ):

    def __init__( self, **opts ):
        multiprocessing.Process.__init__(self)
        self._debug = opts.get("debug", False)
        self._options = opts
        self._run = True

    def run( self ):
        proc_name = self.name
        
        while self._run:
            pass
    

def mapreducer():
    t_size = 100000
    t_interval = (0, 256)
    n_map_procs = 5 # andint( 5,1 )
    n_red_procs = 5 # randint( 5,1 )

    multiprocessing.set_start_method('fork')

    print("[ ] Creating %d map %d reduce processes ..." % ( n_map_procs, n_red_procs ) )
    map_tasks = multiprocessing.JoinableQueue( )
    red_tasks = multiprocessing.JoinableQueue( )
    map_results = multiprocessing.JoinableQueue( )
    red_results = multiprocessing.JoinableQueue( )


    mappers = [ Mapper( map_tasks, map_results ) for i in range( n_map_procs ) ]
    for m in mappers:
        m.start()

    print("[ ] Generating  %d samples in interval %s - %s ..." % ( t_size, t_interval[0], t_interval[1] ) )

    generator = Generator( t_size, len(mappers), t_interval[0], t_interval[1], map_tasks )
    generator.start()

    map_tasks.join()


## ----------------------------------------------------------
## OOP version
## ----------------------------------------------------------
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



## ----------------------------------------------------------
## Utils
## ----------------------------------------------------------
def randint( rng = 10, start=0 ):
    return random.randrange( start, rng )

## ----------------------------------------------------------
## Simple function based
## ----------------------------------------------------------


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


## ----------------------------------------------------------
##  MAIN
## ----------------------------------------------------------

if __name__ == "__main__":

    opt = dict()
#    run_simple()
#    run_oo_version()
    mapreducer()