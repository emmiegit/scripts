#!/usr/bin/env python
from __future__ import print_function
import os
import re
import sys

NUMBERED_FILE_REGEX = re.compile(r'([0-9]+)\.([^ ]+)')

def rename_in_dir(offset, path):
    files = os.listdir(path)
    files.sort()

    if offset > 0:
        files = reversed(files)

    for fn in files:
        match = NUMBERED_FILE_REGEX.match(fn)
        if match is None:
            continue

        number = int(match.group(1))
        new_fn = '{}.{}'.format(number + offset, match.group(2))
        while len(new_fn) < len(fn):
            new_fn = '0' + new_fn

        if os.path.exists(new_fn):
            print("{} already exists! Bailing out.".format(new_fn),
                    file=sys.stderr)
            exit(1)
        print("Renaming: '{}' -> '{}'".format(fn, new_fn))
        os.rename(fn, new_fn)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} [+/-]OFFSET DIRECTORY...".format(sys.argv[0]),
                file=sys.stderr)
        exit(1)

    offset = int(sys.argv[1])
    if offset == 0:
        exit(0)

    paths = sys.argv[2:]
    if not paths:
        paths = ['.']

    for path in paths:
        rename_in_dir(offset, path)

