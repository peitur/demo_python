#!/usr/bin/env python3

import threading
import sys
import os
import pathlib
import time
import signal

class OutputThread( threading.Thread ):
    
    def __init__( self, **opts ):
        super().__init__()
        self.__options = opts.copy()
        self.__in_queue = opts.get("inqueue", None ) 
        self.__out_queue = opts.get("outqueue", None ) 
        self.__run = True
        
    def run( self ):
        while( True ):
            try:
                msg = self.__in_queue.poll():
                print( msg )
            except Exception as e:
                continue                       
            
    def terminate( self ):
        self.__run = False
        
class MainThread( threading.Thread ):
    def __init__( self, **opts ):
        super().__init__()
        self.__options = opts.copy()
        self.__in_queue = opts.get("inqueue", None ) 
        self.__out_queue = opts.get("outqueue", None ) 
        self.__run = True
        
    def run( self ):
        while( self.__run ):
            time.sleep( self.__sleep_time )
            self.__out_queue.put( "ping")
            
    def terminate( self ):
        self.__run = False


if __name__ == "__main__":
    
    m_th = MainThread( )