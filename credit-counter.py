#!/usr/bin/env python
"""
Automatically counts credits in CYOA-type games by looking
for instances of +(number) and -(number) and adding it all up.
"""

from __future__ import print_function, with_statement
import re
import os
import sys

CREDIT_REGEX = re.compile(r'([+-][0-9]+)')
MONEY_REGEX = re.compile(r'([+-]\$[0-9]+(?:\.[0-9]+)?k?)', re.IGNORECASE)

def count_credits(text):
    transactions = CREDIT_REGEX.findall(text)
    credits = 0

    for transaction in transactions:
        credits += int(transaction)

    return credits

def count_dollars(text):
    transactions = MONEY_REGEX.findall(text)
    money = 0.0

    for transaction in transactions:
        mult = 1
        transaction = transaction.replace('$', '')
        if transaction.endswith('k', re.IGNORECASE):
            mult = 1000
            transaction = transaction[:-1]
        money += float(transaction) * mult

    return money

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage:\n%s path-to-file..." % os.path.basename(sys.argv[0]))
        exit(1)

    for fn in sys.argv[1:]:
        with open(fn, 'r') as fh:
            text = fh.read()

        credits = count_credits(text)
        money = count_dollars(text)
        if money:
            print("%s: %d credits, $%.02f per interval" % (fn, credits, money))
        else:
            print("%s: %d credits" % (fn, credits))

