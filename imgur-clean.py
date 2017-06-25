#!/usr/bin/env python3

"""
"imgur-album-downloader" is great, but it seems to download
albums twice, and appends their stupid ID to the end.
This script fixes both.
"""

import hashlib
import re
import os
import sys

IMGUR_FILENAME_REGEX = re.compile(r'([0-9]+)(?:-\w+)?\.([A-Za-z0-9]+)')

def get_hash(fn):
    with open(fn, 'rb') as fh:
        hashsum = hashlib.md5(fh.read()).digest()
    return hashsum

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        os.chdir(sys.argv[1])

    sums = {}

    for fn in os.listdir('.'):
        match = IMGUR_FILENAME_REGEX.match(fn)
        if match is None:
            continue

        new_fn = f'{match.group(1)}.{match.group(2)}'
        if fn == new_fn:
            continue

        print(f"Renaming '{fn}' to '{new_fn}'")
        os.rename(fn, new_fn)
        hashsum = get_hash(new_fn)
        files = sums.get(hashsum, [])
        files.append(new_fn)
        sums[hashsum] = files

    for hashsum, files in sums.items():
        if len(files) > 1:
            files_quoted = [f"'{x}'" for x in files]
            print(f"Found duplicates: {', '.join(files_quoted)}")
            files.sort()
            for fn in files[1:]:
                os.remove(fn)

