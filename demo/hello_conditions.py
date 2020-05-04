#!/usr/bin/env python3



if __name__ == "__main__":

    nothing = None
    a_string = "hello"
    an_integer = 3
    a_boolean = False
    CONTANT_PI = 3.14

    if not nothing:
        print( "nothing is nothing" )

    if a_string == "hello":
        print("welcome")
    elif a_string == "world":
        print("planet")
    else:
        print("go figure")

    if an_integer < 0:
        print("found some caves")
    elif an_interger > 0:
        print("to the sky")
    else:
        print("land ohoy")

    if a_boolean:
        print("need no more")
    else:
        print("still")
