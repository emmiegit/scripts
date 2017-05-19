#!/usr/bin/env python
"""
Automatically counts credits in CYOA-type games.
"""

from __future__ import print_function, with_statement
import re
import os
import sys

COMMENT_REGEX = re.compile(r'^\s*#')
RESET_REGEX = re.compile(r'\s*%reset(?:\s+([A-Za-z]))?\s*', re.IGNORECASE)
CREDIT_REGEX = re.compile(r'[^0-9]([+-][0-9]+)\s*([A-Za-z_]*)[^0-9%]')
MONEY_REGEX = re.compile(r'([+-])\$([0-9]+(?:\.[0-9]+)?k?)', re.IGNORECASE)

def get_sign(s):
    if s == '-':
        return -1.0
    else:
        return +1.0

def get_reset(text):
    match = RESET_REGEX.match(text)
    if match:
        coin = match.group(1)
        return coin if coin else ''

def count_credits(credits, text):
    matches = CREDIT_REGEX.finditer(text)

    for match in matches:
        amount = match.group(1)
        coin = match.group(2)
        credits[coin] = credits.get(coin, 0) + int(amount)

def count_dollars(text):
    matches = MONEY_REGEX.finditer(text)
    money = 0.0

    for match in matches:
        mult = 1
        sign = get_sign(match.group(1))
        amount = match.group(2)
        if amount.endswith('k', re.IGNORECASE):
            mult = 1000
            amount = amount[:-1]
        money += sign * float(amount) * mult
    return money

def print_results(fn, credits, money):
    credit_parts = []
    for key in sorted(credits.keys()):
        if key:
            credit_parts.append("%d '%s' credits" % (credits[key], key))
        else:
            credit_parts.append("%d credits" % credits[key])
    if money:
        credit_parts.append("$%.02f per interval" % money)

    if credit_parts:
        padding = ' ' * (len(fn) + 2)
        credit_str = ('\n' + padding).join(credit_parts)
    else:
        credit_str = "(none)"
    print("%s: %s" % (fn, credit_str))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        inputs = [("<stdin>", sys.stdin.readlines())]
    else:
        inputs = []
        for fn in sys.argv[1:]:
            with open(fn, 'r') as fh:
                inputs.append((fn, fh.readlines()))

    for fn, lines in inputs:
        credits = {}
        money = 0.0

        for line in lines:
            if COMMENT_REGEX.match(line):
                continue
            reset = get_reset(line)
            if reset:
                credits[reset] = min(credits[reset], 0)
            count_credits(credits, line)
            money += count_dollars(line)
        print_results(fn, credits, money)

