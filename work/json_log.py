#!/usr/bin/env python3
from pprint import pprint
import json
import sys

def pipe(line):
    try:
        log = json.loads(line)
        try:
            print("[{}] {}{} {}: {}".format(
                log['level'].upper(),
                log['time'],
                log['ms'],
                log['name'],
                log['event'],
            ))

            if log['event'] == 'error':
                print(log['meta']['error']['stack'])
        except KeyError:
            pprint(log)
    except json.decoder.JSONDecodeError:
        sys.stdout.write(line)

    sys.stdout.flush()

if __name__ == '__main__':
    for line in sys.stdin:
        pipe(line)
