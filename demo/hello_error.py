#!/usr/bin/env python3

# Error handling: https://docs.python.org/3/tutorial/errors.html
# Exceptions: https://docs.python.org/3/library/exceptions.html
# Stack trace back: https://docs.python.org/3/library/traceback.html

import sys, traceback

if __name__ == "__main__":
    print("\n##################################################################")

    try:
        filename = sys.argv[1]
        f = open( filename, 'r')
        print("File bytes: %s" % ( len( f.read( -1 ) ) ))
    except IndexError as e:
        print("Oppos!! missing indata, filename required")
    except OSError as e:
        print("Failed to open file %s" % ( filename ) )
    except Exception as e:
        print("Unhandled error: %s" % (e) )
        raise
    else:
        print("# Cleanup calling ...")
        f.close()
    finally:
        print("# finishing this up ...")


    print("\n##################################################################")

    print("\n### Detailed exception output:" )
    try:
        print( sys.argv[1] )
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("\n*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

        print("\n*** print_exception:")
        # exc_type below is ignored on 3.5 and later
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print("\n*** print_exc:")
        traceback.print_exc(limit=2, file=sys.stdout)

        print("\n*** format_exc, first and last line:")
        formatted_lines = traceback.format_exc().splitlines()
        print(formatted_lines[0])
        print(formatted_lines[-1])

        print("\n*** format_exception:")
        # exc_type below is ignored on 3.5 and later
        print(repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback)))
        print("\n*** extract_tb:")
        print(repr(traceback.extract_tb(exc_traceback)))

        print("\n*** format_tb:")
        print(repr(traceback.format_tb(exc_traceback)))

        print("\n*** tb_lineno:", exc_traceback.tb_lineno)
