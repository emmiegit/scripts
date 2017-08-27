#!/usr/bin/env python
import os
import random
import shutil
import sys

def sample(src, dest, amount):
    files = []
    for dir_path, _, dir_files in os.walk(src):
        files += map(lambda x: os.path.join(dir_path, x), dir_files)
    random.shuffle(files)

    if len(files) < amount:
        print(f"Not enough files to select {amount} (only {len(files)}).")

    for i, fn in enumerate(files[:amount]):
        if '.' in fn:
            ext = fn.split('.')[-1]
            newfn = f'{i:04}.{ext}'
        else:
            newfn = f'{i:04}'

        path = os.path.join(dest, newfn)
        print(f'{fn} -> {path}')
        shutil.copyfile(fn, path)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Not enough arguments.")
        print(f"Usage: {sys.argv[0]} [source directory] [output directory] [amount]")
        exit(1)

    src = sys.argv[1]
    if not os.path.isdir(src):
        print(f"Error: directory does not exist: '{src}'")
        exit(1)

    dest = sys.argv[2]
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except:
        print(f"Error: cannot make directory: '{dest}'")
        exit(1)

    try:
        amt = int(sys.argv[3])
        if amt < 0:
            raise ValueError
    except:
        print(f"Error: must enter positive integer, not '{sys.argv[3]}'")
        exit(1)

    sample(src, dest, amt)
