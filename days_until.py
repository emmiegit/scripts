#!/usr/bin/env python
from __future__ import with_statement
import argparse, math, re, time, os, sys

SECONDS_PER_DAY = 86400
EVENT_FILE = os.path.dirname(sys.argv[0]) + os.sep + "eventlist.txt"
EVENT_RE = re.compile("([A-Z][a-z]{2} [0-9]{2} [0-9]{4}) (.*)\n")

TODAY = int(time.time())

def get_events(fn):
    past = []
    future = []
    try:
        with open(fn, 'r') as fh:
            line = fh.readline()
            while line:
                match = EVENT_RE.match(line)
                if match:
                    date = time.mktime(time.strptime(match.group(1), "%b %d %Y"))
                    name = match.group(2)
                    days = (TODAY - int(date)) / SECONDS_PER_DAY
                    if days >= 0:
                        past.append((days, name))
                    else:
                        future.append((-days, name))
                line = fh.readline()
    except StandardError as err:
        print(err)
        exit(1)

    past.sort()
    future.sort()

    if not (past or future):
        # Event list is empty
        width = 1
    else:
        # Calculate number of digits
        width = math.ceil(math.log10(max(past[-1][0], future[-1][0])))
    return past[::-1], future, width

def print_past_events(args, past, width):
    if args.nopast:
        form = "%%%dd day%%c since %%s" % width
        for event in past:
            if not args.delta or event[0] <= args.delta:
                fargs = (event[0], ' ' if event[0] == 1 else 's', event[1])
                print(form % fargs)

def print_future_events(args, future, width):
    if args.nofuture:
        form = "%%%dd day%%c until %%s" % width
        for event in future:
            if not args.delta or event[0] <= args.delta:
                fargs = (event[0], ' ' if event[0] == 1 else 's', event[1])
                print(form % fargs)

if __name__ == "__main__":
    # Parse options with argparse
    argparser = argparse.ArgumentParser(description="List events by days since/until they happen(ed).")
    argparser.add_argument("-d", "--delta", default="0", help="Only print events whose days since/until is less than this argument. (0 for no limits)")
    argparser.add_argument("-i", "--input", default=EVENT_FILE, help="Specify a different input other than \"eventlist.txt\".")
    argparser.add_argument("-r", "--reverse", action="store_true", help="Print the events in reverse order.")
    argparser.add_argument("-n", "--nopast", action="store_false", help="Don't print any events that have already happened.")
    argparser.add_argument("-N", "--nofuture", action="store_false", help="Don't print any events that haven't happened yet.")
    args = argparser.parse_args()

    try:
        args.delta = int(args.delta)
        if args.delta < 0:
            raise ValueError
    except:
        print("Delta must be a positive integer.")
        exit(1)

    # Fetch event data
    past, future, width = get_events(args.input)

    if args.reverse:
        print_future_events(args, reversed(future), width)
        print_past_events(args, reversed(past), width)
    else:
        print_past_events(args, past, width)
        print_future_events(args, future, width)

