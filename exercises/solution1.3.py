#!/usr/bin/env python3
import os, sys, re

def instance( obj, t ):
    if type( obj ).__name__ == t:
        return True
    return False

if __name__ == "__main__":

    script = sys.argv.pop(0)
    item = sys.argv.pop(0)
    value = sys.argv.pop(0)

    p = re.split("/", item )
    