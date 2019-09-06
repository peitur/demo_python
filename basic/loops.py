#!/usr/bin/env python3

##########################################################
## Part 1, simpole loops
##########################################################
def loop_part1():
    pass

##########################################################
## Part 2, looping structures
##########################################################
def loop_part2_list():
    ## empty list of whatever, empty
    list0 = list()
    list1 = []

    list3 = ["a", "b", "c","d" ]


    print("############# LIST ##############")
    print("Sample [%s]: %s" % ( len(list3), list3 ) )

    print("\n## Print list as is:")
    for x in list3:
        print(x)

    print("\n## Sorted list:")
    for x in sorted( list3 ):
        print(x)

    print("\n## Print list enumerated:")
    for a, b  in enumerate( list3 ):
        print( "%s => %s" % (a, b) )

    print("\n## Print with list comprehension:")
    [ print( x ) for x in list3 ]


def loop_part2_dict():

    print("############# DICTS ##############")
    ## empty dictionary, empty
    dict0 = dict()
    dict1 = {"a": "alfa", "b":"beta", "c": "hmmm", "g": "gama"}

    print("\n# print keys")
    for x in dict1:
        print(x)

    print("\n# print keys and values:")
    for x in dict1:
        print("%s => %s" % ( x, dict1[x]) )

    print("\n# print enumerated keys and values:")
    for a,b in enumerate( dict1 ):
        print("%d => %s => %s" % ( a, b, dict1[b] ) )

    print("\n# print with list comprehension (list version):")
    [ print( x ) for x in dict1 ]

    print("\n# print with list comprehension (dict version):")
    { print( x ) for x in dict1 }

if __name__ == "__main__":

    ##########################################################
    ## Part 1, simpole loops
    ##########################################################



    ##########################################################
    ## Part 2, looping structures
    ##########################################################
    loop_part2_list()
    loop_part2_dict()

    ##########################################################
    ## Part 3, iterators
    ##########################################################
