#!/usr/bin/env python3

import re
import os
import sys

HASH_LIST_REGEX = re.compile(r'"(.*)" -> "(.*)"\s*')

def rename(old, new):
    if not os.path.exists(old):
        print("'{}' doesn't exist".format(old))
    elif os.path.exists(new):
        print("'{}' already exists, not overwriting".format(new))
    elif old == new:
        print("Source and destination are the same ({})".format(old))
    else:
        print("'{}' -> '{}'".format(old, new))
        os.rename(old, new)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        fn = 'hash-renamed-files.txt'
    else:
        fn = sys.argv[1]

    if not os.path.isfile(fn):
        print("Can't find '{}'".format(fn))
        exit(1)

    with open(fn, 'r') as fh:
        for line in fh.readlines():
            match = HASH_LIST_REGEX.match(line)
            if match is None:
                print("Non-matching line: '{}'".format(line.rstrip()))
            else:
                rename(match[2], match[1])

