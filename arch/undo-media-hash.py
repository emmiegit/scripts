#!/usr/bin/env python
import sys, os
CONFIRM_ALL = False

def confirmation():
    global CONFIRM_ALL
    if CONFIRM_ALL:
        return True
    else:
        response = raw_input("Ok? [Y/n/a/q] ").lower().strip()
        if response in ("", "y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        elif response in ("a", "always"):
            CONFIRM_ALL = True
            return True
        elif response in ("q", "quit"):
            sys.exit(1)
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "hash_renamed_files.txt"

    fh = open(fn, 'r')
    lines = fh.readlines()
    import os
    for line in lines:
        orig, curr = line.split(" -> ")

        if CONFIRM_ALL:
            print("%s -> %s" % (curr, orig))
        else:
            sys.stdout.write("%s -> %s: " % (curr, orig))

        if confirmation():
            try:
                os.rename(curr.strip()[1:-1], orig.strip()[1:-1])
            except:
                sys.stderr.write("Unable to rename %s -> %s.\n" % (curr, orig))

