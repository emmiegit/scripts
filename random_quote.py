#!/usr/bin/env python
from __future__ import print_function, with_statement
import glob
import os
import random
import sys
import time


def aggregate_quotes(files):
    quotes = {}

    for fn in files:
        try:
            with open(fn, 'r') as fh:
                quotes[fn] = fh.read().split("%")
        except Exception as ex:
            print("Unable to open file \"%s\": %s." % (fn, ex))

    return quotes


def random_quote(quotes):
    all_quotes = []

    for source, quote_list in quotes.items():
        for quote in quote_list:
            all_quotes.append((quote.strip(), source))

    return random.choice(all_quotes)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        files = glob.glob("*.txt")
    else:
        files = sys.argv[1:]

    quotes = aggregate_quotes(files)
    this_file = sys.argv[0].lower()

    if not quotes:
        print("No quotes found.")
        sys.exit(0)

    daily_quotes = os.path.basename(this_file) == "daily_quote.py"

    if daily_quotes:
        loc = time.localtime()
        random.seed(loc.tm_year << 16 | loc.tm_yday)

    quote, source = random_quote(quotes)

    if daily_quotes:
        print("Today's quote is from %s:\n\n%s" % (source, quote))
    else:
        print("Here is a quote from %s:\n\n%s" % (source, quote))

