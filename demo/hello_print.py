#!/usr/bin/env python3

import sys
import time
from pprint import pprint

if __name__ == "__main__":

    print("your message")
    print("your message", file=sys.stdout )
    print("your message", file=sys.stderr)
    print("your message", end="" )

    byteBuffer = 1024
    bytesLoaded = 0
    size = 10240
    print("\nstart\n")
    while bytesLoaded < size:
        bytesLoaded += byteBuffer
        print("Loaded [ %10d / %-10d ] ..." % (  bytesLoaded, size ), end="\r", flush=True )
        time.sleep(0.5)
    print("\ndone\n")
