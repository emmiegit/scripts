#!/usr/bin/python

from pprint import pprint
import pickle
import sys

if __name__ == '__main__':
    ret = 0

    for fn in sys.argv[1:]:
        print("Contents of '%s':" % fn)
        try:
            with open(fn, 'rb') as fh:
                obj = pickle.load(fh)
            pprint(obj)
        except Exception as ex:
            print("Failure: %r" % ex)
            ret = 1

        if fn is not sys.argv[-1]:
            print()

    exit(ret)

