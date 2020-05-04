#!/usr/bin/env python3

import os, sys, re, socket, struct
import dpkt
import pcapy
import socket
import signal

from pprint import pprint

class Capture( object ):
    def __init__( self, dev ):
        self._device = dev
        self._caph = None
        self._fd = None
        self._filter = None
        self._max_len = 65536
        self._timeout = 10

    def open( self ):
        try:

            self._caph = pcapy.open_live( self._device , self._max_len, True, self._timeout )
            self._fd = self._caph.getfd()
            if self._filter:
                self._caph.setfilter( self._filter )

        except Exception as e:
            pprint( e )

    def read( self ):
        while True:
            try:
                (header, packet) = self._caph.next()
                eth = dpkt.ethernet.Ethernet(packet)
#                print( "ETH: From: %s Type: %s" % ( eth.src, eth.type ) )
                if eth.type == dpkt.ethernet.ETH_TYPE_ARP:
                    arp = eth.data
                    print("ARP FROM %s"% ( arp.spa ) )
                elif eth.type == dpkt.ethernet.ETH_TYPE_IP:
                    ip = eth.data
                    pprint( ip )
                else:
                    pprint( eth )

            except Exception as e:
                print("ERROR CAP: %s" % ( e ) )

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal( signal.SIGINT, handler )
    if len( sys.argv ) == 2:
        print("My IP: %s" % ( socket.gethostbyname(socket.gethostname()) ) )
        cap = Capture( sys.argv[1] )
        cap.open()
        cap.read()
