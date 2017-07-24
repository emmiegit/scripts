#!/usr/bin/python

from pprint import pprint
import argparse
import os
import pickle
import sys

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-I', '--import', dest='modules', action='append',
            help="List of modules to import before dumping the pickle.")
    argparser.add_argument('filenames', nargs='+',
            help="List of files to inspect.")
    args = argparser.parse_args()

    for module in args.modules:
        exec(f"import {module}")

    success = True
    for fn in args.filenames:
        print(f"Contents of '{fn}':")
        try:
            with open(fn, 'rb') as fh:
                obj = pickle.load(fh)
            pprint(obj)
        except Exception as ex:
            print(f"Failure: {ex!r}")
            success = False

    exit(int(success))

