#!/usr/bin/env python3 -m unittest

# python -m unittest hello_testing.py

import unittest
import sys

from pprint import pprint

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSomethingAAAAAA('testing_something_1'))
    suite.addTest(TestSomethingBBBBBB('testing_something_2'))
    return suite

class TestSomethingAAAAAA(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown( self ):
        pass

    def test_int_equals( self ):
        self.assertEqual( "abc", "abc" )

    def test_int_a_in_str( self ):
        self.assertIn( "b", "abc" )

class TestSomethingBBBBBB(unittest.TestCase):

    def setUp(self):
        self._ints = [1,2,3,4,5,6,7,8]

    def tearDown( self ):
        pass

    def test_int_equals( self ):
        self.assertEqual( 1, 1 )

    def test_int_not_equals( self ):
        self.assertNotEqual( 1,2 )

    def test_int_in_list( self ):
        self.assertIn( 3, self._ints )

    def test_int_not_in_list( self ):
        self.assertNotIn( 30, self._ints )

if __name__ == "__main__":
#    runner = unittest.TextTestRunner( stream=sys.stderr, descriptions=True, verbosity=2, failfast=False ).run( suite() )
    unittest.main( verbosity=2 )
