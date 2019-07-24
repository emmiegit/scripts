#!/usr/bin/python3

from pprint import pprint
import json
import sys

def get(obj, path):
    try:
        for part in path:
            obj = obj[part]
        return obj
    except KeyError:
        return None

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        paths = [sys.argv[1].split('.')]
    else:
        paths = [
            ['meta', 'error', 'stack'],
            ['error', 'stack'],
            ['traceback'],
        ]

    obj = json.load(sys.stdin)

    for path in paths:
        subobj = get(obj, path)
        if subobj is not None:
            obj = subobj
            break

    if isinstance(obj, str):
        print(obj)
    else:
        pprint(obj)
