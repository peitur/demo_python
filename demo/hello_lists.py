#!/usr/bin/env python3

from pprint import pprint
if __name__ == "__main__":

    ## empty list of whatever, empty
    list0 = list()

    print("\n# Supported object fuctions and functionality")
    pprint( dir( list0 ) )

    ## creting a simple list of numbers
    list1 = [ 103, 101, 108, 114, 105 ]

    ## reference copy of list1
    list2 = list1

    ## copying the list into a new list (copy, not reference)
    list3 = list1.copy()

    list4 = ["a","b","c","d","e","f","g","h","i","j","k","l"]

    print("\n# start list")
    pprint( list1 )

    list1.append( 201 )
    list1.append( 202 )
    list2.reverse()

    print("\n# original list, appendded 2 elements and reversed")
    pprint( list1 )

    ## list comprehension,
    print("\n# list comprehension")
    pprint( [ x + x for x in list1 ] )

    ## map funciton, takes a transform (map) function and a list (or iterable) object
    print("\n# map funciton result")
    pprint( list( map( lambda x: x + x, list1 ) ) )

    ## Since we copied list1 to list2, it's not just a reference.
    print( "\n# list2, created as reference")
    pprint( list2 )

    print("\n# list3, copy of list1")
    pprint( list3 )

    print("\n# element in list4")
    if "a" in list4:
        print("a is in list4")

    print("\n# lets print a list with indexes" )
    for i, e in enumerate( list1 ):
        print("%d > %s" % ( i, e ) )

    print("\n# basically, enumerate gives us a list/iterable of tuples")
    pprint(  list( enumerate( list1 ) ) )

    print("\n## Joining lists")
    print( ", ".join( list4 ) )

    print("\n## Map lists")
    print( list(map(lambda x: x * x, range(10))) )

    ######################################################
    print("\n# Using lists as stacks")


    ## in stacks, we put data ontop and remove the most top elment all the time
    data = ("aaaa","bbbb","cccc")
    stack = list()
    for elem in data:
        print("# append '%s'" % ( elem ) )
        stack.append( elem )

    pprint(stack)
    print("# pop last element")
    pprint( stack.pop() )
    pprint( stack )

    ######################################################
    print("\n# Using lists as queue")

    ## in queues, we insert elements on the top and extract data in the other end
    data = ("xxxx","zzzzz","wwwww" )
    queue = list()
    for elem in data:
        print("# append '%s'" % ( elem ) )
        queue.append( elem )

    pprint(queue)
    print("# pop most left element")
    pprint( queue.pop( 0 ) )
    pprint( queue )

    ######################################################
