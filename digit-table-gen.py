#!/usr/bin/env python
from __future__ import print_function
import sys

def print_binary_table(digits):
    for i in range(1 << digits):
        bn = bin(i)[2:]
        print(' & '.join(bn.rjust(digits, '0')), end='')
        print(" \\\\")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s digits..." % sys.argv[0])
        exit(1)

    for arg in sys.argv[1:]:
        digits = int(arg)
        if digits <= 0:
            raise ValueError("Given value is negative or zero: %s" % arg)

        print_binary_table(digits)

