#!/usr/bin/env python
import os, random, shutil, sys

def sample(src, dest, amount):
    files = os.walk(src).next()[2]
    random.shuffle(files)

    print(files)
    if len(files) < amount:
        print "Not enough files to select %d (only %d)." % (amount, len(files))
    
    for i in range(amount):
        fn = files.pop()
        ext = fn.split(".")[-1]
        newfn = "%s%s%04d.%s" % (dest, os.sep, i, ext)
        print "%s -> %s" % (fn, newfn)
        shutil.copyfile("%s%s%s" % (src, os.sep, fn), newfn) 

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print("Not enough arguments.")
        print("Usage: %s [source directory] [output directory] [amount]" % sys.argv[0].split(os.sep)[-1])
        exit(1)
    
    src = sys.argv[1]
    if not os.path.isdir(src):
        print("Error: directory does not exist: \"%s\"." % src)
        exit(1)
    
    dest = sys.argv[2]
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
        if not os.path.isdir(dest):
            raise ValueError
    except:
        print("Error: cannot make directory: \"%s\"." % dest)
        exit(1)

    try:
        amt = int(sys.argv[3])
        if amt < 0:
            raise ValueError
    except:
        print("Error: must enter positive integer, not \"%s\"." % sys.argv[3])
        exit(1)

    sample(src, dest, amt)

