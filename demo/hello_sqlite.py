#/usr/bin/env python3

import os, sys
import sqlite3

FILENAME=".demo.db"

class DemoDatabase( object ):

    def __init__( self, filename, **opt ):
        self._filename = filename
        self._conn = sqlite3.connect( self._filename )

    def __init__db( self ):

        self._tables = dict()


    def __commit_db( self ):

        try:
            if self._conn:
                self._conn.commit()
        except Exception as e:
            raise e

    def close( self ):
        if self._conn:
            self._conn.close()

    def create( self ):
        return self.__init__db()

    def reset( self ):
        pass

    def insert( self, table, mp = {} ):
        pass

    def select( self, table, fields=[], where=[] ):
        pass

    def update( self, table, idname, idvalue, field, value ):
        pass

    def delete( self, table, idname, idvalue ):
        pass


if __name__ == "__main__":
    pass
