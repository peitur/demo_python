#!/usr/bin/env python3

from pprint import pprint

class Test1( object ):

    def __init__( self, param ):
        self._param = param
        self._type = type( param ).__name__

    def getType( self ):
        return self._type

    def getParam( self ):
        return self._param

    def __str__( self ):
        return "%s:%s" % ( self._param.__str__(), self._type.__str__() )

    def create( param ):
        return Test1( param )

class Test2( Test1 ):

    def __init__( self, param, data ):
        Test1.__init__(self, param )
        self._data = data

    def __str__( self ):
        return "%s;%s" % ( super().__str__(), self._data.__str__()  )

    def create( param, data = "oops" ):
        return Test2( param, data )

if __name__ == "__main__":

    print("#"*32)
    pprint( dir( Test2 ))
    print("#"*32)

    print( Test1( "test" ) )
    print( Test1.create( "hello" ) )
    print( Test2( "foo", "bar" ) )
    print( Test2.create( "foo" ) )
