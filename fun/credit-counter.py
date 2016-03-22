#!/usr/bin/env python
"""
Automatically counts credits in CYOA-type games by looking
for instances of +(number) and -(number) and adding it all up.
"""

from __future__ import with_statement
import re
import os
import sys

CREDIT_REGEX = re.compile(r"([+-][0-9]+)")


def count_credits(text):
    transactions = CREDIT_REGEX.findall(text)
    credits = 0

    for transaction in transactions:
        credits += int(transaction)

    return credits


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n%s path-to-file..." % os.path.basename(sys.argv[0]))
        exit(1)

    for fn in sys.argv[1:]:
        with open(fn, 'r') as fh:
            credits = count_credits(fh.read())
            print("%s: %d credits" % (fn, credits))

