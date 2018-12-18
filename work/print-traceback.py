#!/usr/bin/python3

from pprint import pprint
import json
import sys

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        path = sys.argv[1].split('.')
    else:
        path = ['error', 'stack']

    obj = json.load(sys.stdin)

    try:
        for part in path:
            obj = obj[part]
    except KeyError:
        pass

    if isinstance(obj, str):
        print(obj)
    else:
        pprint(obj)
