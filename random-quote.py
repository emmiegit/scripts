#!/usr/bin/python3

import os
import random
import re
import sys
import time

DAILY_QUOTE_FILE_NAME_REGEX = re.compile(r"daily.quotes?\.py", re.IGNORECASE)

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
        files = ['qotd-list.txt']
    else:
        files = sys.argv[1:]

    quotes = aggregate_quotes(files)

    if not quotes:
        print("No quotes found.")
        sys.exit(1)

    this_file = os.path.basename(sys.argv[0])
    daily_quotes = bool(DAILY_QUOTE_FILE_NAME_REGEX.match(this_file))

    if daily_quotes:
        loc = time.localtime()
        random.seed(loc.tm_year << 16 | loc.tm_yday)

    quote, source = random_quote(quotes)

    if daily_quotes:
        print("Today's quote is from %s:\n\n%s" % (source, quote))
    else:
        print("Here is a quote from %s:\n\n%s" % (source, quote))
