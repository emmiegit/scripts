#!/usr/bin/env python3

"""
"imgur-album-downloader" is great, but it seems to download
albums twice, and appends their stupid ID to the end.
This script fixes both.
"""

import re
import os
import sys

IMGUR_FILENAME_REGEX = re.compile(r'([0-9]+)-(\w+)\.([A-Za-z0-9]+)')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        os.chdir(sys.argv[1])

    ids = {}

    for fn in os.listdir('.'):
        match = IMGUR_FILENAME_REGEX.match(fn)
        if match is None:
            continue

        new_fn = f'{match[1]}.{match[3]}'
        if fn == new_fn:
            continue

        print(f"Renaming '{fn}' to '{new_fn}'")
        os.rename(fn, new_fn)
        id = match[2]
        files = ids.get(id, [])
        files.append(new_fn)
        ids[id] = files

    for _, files in ids.items():
        if len(files) > 1:
            files_quoted = ', '.join(f"'{fn}'" for fn in files)
            print(f"Found duplicates: {files_quoted}")
            files.sort()
            for fn in files[1:]:
                print(f"Removing {fn}")
                os.remove(fn)

