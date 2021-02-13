#!/usr/bin/env python3

# Move all files into a directory to the current directory,
# then delete the directory

import argparse
import os
import sys


def check_conflicts(directories, destination):
    conflits = []

    for directory in directories:
        for filename in os.listdir(directory):
            if os.path.exists(os.path.join(destination, filename)):
                conflicts.append(os.path.join(directory, filename))

    return conflicts


def splat(directory, destination, verbose=False):
    for filename in os.listdir(directory):
        src = os.path.normpath(os.path.join(directory, filename))
        dest = os.path.normpath(os.path.join(destination, filename))

        if verbose:
            print(f"renamed '{src}' -> '{dest}'")
        os.replace(src, dest)

    if verbose:
        print(f"removed '{directory}'")
    os.rmdir(directory)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Flatten a directory, moving all its contents into the current directory.",
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Execute verbosely, printing out each action taken",
    )
    argparser.add_argument(
        "-n",
        "--no-clobber",
        dest="no_clobber",
        action="store_true",
        help="Do not clobber existing files: error if conflicts are encountered",
    )
    argparser.add_argument(
        "-d",
        "--destination",
        dest="destination",
        default=".",
        help="The directory to move flattened files into",
    )
    argparser.add_argument(
        "directory",
        nargs="+",
        help="The directories to be acted upon",
    )
    args = argparser.parse_args()

    if args.no_clobber:
        conflicts = check_conflicts(args.directory, args.destination)
        if conflicts:
            conflicts_fmt = "\n".join(f" * {path}" for path in conflicts)
            print(f"Cannot splat, would clobber existing files:\n{conflicts_fmt}", file=sys.stderr)
            sys.exit(1)

    for directory in args.directory:
        splat(directory, args.destination, args.verbose)
