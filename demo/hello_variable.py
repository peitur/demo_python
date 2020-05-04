#!/usr/bin/env python3

from pprint import pprint

if __name__ == "__main__":

    a_bool = False
    a_string = "hello string"
    an_integer = 42
    a_float = 3.14
    A_CONST = 3.14
    a_anon_f = lambda x, y: x * y

    ## Everything is references, chainging copies also changes original

    # tuples can be nested
    # tuple are immutable
    a_tuple = 1,2,3,4,"a","b"

    a_list1 = []
    a_list2 = list()
    a_list3 = [1,2,"a","b"]

    a_dict1 = {}
    a_dict2 = dict()
    a_dict3 = {"name":"test", "type":"sample", "tags":["sample"]}

    a_set1 = {}
    a_set2 = set()
    a_set3 = {"a","b","c", "a", "b", "c"}
