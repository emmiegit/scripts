#!/usr/bin/env python
# Identify images smaller than a given resolution and print their file names.
from __future__ import print_function
import os, sys, subprocess

IMAGE_FILES = ("jpg", "jpeg", "png", "tif", "tiff")

def main(directory, end, min_width, min_height):
    for dirpath, dirs, files in os.walk(directory):
        os.chdir(dirpath)
        for fn in files:
            if fn.lower().split('.')[-1] in IMAGE_FILES:
                try:
                    size = subprocess.check_output(["identify", "-format", "%[fx:w]x%[fx:h]", fn])
                except subprocess.CalledProcessError as err:
                    print("Error getting size for \"%s\": %s" % (os.path.abspath(fn), err))
                    continue

                width, height = size.split(b'x')

                if int(width) < min_width or int(height) < min_height:
                    print(os.path.abspath(fn), end=end)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: %s directory min-width min-height" % (os.path.basename(sys.argv[0])), file=sys.stderr)
        sys.exit(1)

    source = sys.argv[1]
    if not os.path.isdir(source):
        print("Location does not exist or is not a directory: \"%s\"." % source, file=sys.stderr)
        sys.exit(1)

    try:
        width = int(sys.argv[2])
    except:
        print("Invalid width: %s" % (sys.argv[2]), file=sys.stderr)
        sys.exit(1)

    try:
        height = int(sys.argv[3])
    except:
        print("Invalid height: %s" % (sys.argv[3]), file=sys.sterr)
        sys.exit(1)

    try:
        main(source, '\n', width, height)
    except KeyboardInterrupt:
        print("Caught user interrupt, quitting.", file=sys.stderr)
        sys.exit(1)

