#!/usr/bin/env python3

if __name__ == "__main__":

    ## empty list of whatever, empty
    str0 = ""
#    print( dir( str0 ) )

    print("#################################################")
    ## simple build stringh with variables
    print( "\n[s1] hello %s and %s" % ( "world", "others" ) )
    print( "\n[s2] hello %30s again" % ( "world" ) )
    print( "\n[s3] hello %-30s again" % ( "world" ) )
    print( "\n[s4] hello again for the %d time" % ( 10 ) )
    print( "\n[s5] hello %(name)s for %(time)s" % { "time":"last", "name":"world" } )
