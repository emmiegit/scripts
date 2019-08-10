#!/usr/bin/python3

import sys

def generate_tabs(start=None, stop=None):
    start = 0 if start is None else start
    stop = 4999 if stop is None else stop

    lines = ['[[tabview]]']

    for num in range(start, stop + 1):
        lines.extend((
            f'[[tab {num:03}]]',
            #f'[[include :scp-wiki:scp-{num:03}]]',
            '[[/tab]]',
        ))

    lines.append('[[/tabview]]')
    return '\n'.join(lines)

if __name__ == '__main__':
    start, stop = None, None

    if len(sys.argv) > 2:
        stop = int(sys.argv[2])
    if len(sys.argv) > 1:
        start = int(sys.argv[1])

    print(generate_tabs(start, stop))
