#!/usr/bin/env python3
# Run python3, where ever it is

# Buildin __name__ contains name of module.
# as in other languages, main is entrypoint, this is where everything starts in some way.
# This is only "__main__" in the main executable
if __name__ == "__main__":

  # Scope defined by indentation, tab or space.
  # The type must be consistent!

  # Lets just print something
  print("Hello world")

  # lets print __name__
  print("Hello %s" % ( __name__ ))
