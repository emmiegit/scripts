#!/usr/bin/env python3

import hashlib
import os
import sys


def normalize_algorithm(name):
    # Since the name might be caps or have dashes,
    # we normalize to lowercase as used by Python's hashlib.

    return name.lower().replace("-", "")


def plural(number):
    return "" if number == 1 else "s"


def hash_rename(algorithm, path, errors):
    try:
        with open(path, "rb") as file:
            data = file.read()

        hasher = hashlib.new(algorithm, data)
        digest = hasher.hexdigest()

        directory = os.path.dirname(path)
        _, ext = os.path.splitext(path)
        new_path = os.path.join(directory, digest + ext)

        if os.path.exists(new_path):
            raise RuntimeError(
                f"Destination path '{new_path}' (from '{path}') already exists",
            )

        print(f"Renaming {path} -> {new_path}")
        os.rename(path, new_path)
    except Exception as error:
        errors.append(error)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <algorithm> <path...>")
        sys.exit(1)

    algorithm = normalize_algorithm(sys.argv[1])
    paths = sys.argv[2:]

    print(f"Hashing {len(paths)} files{plural(len(paths))} with {algorithm}")
    errors = []

    for path in paths:
        hash_rename(algorithm, path, errors)

    if errors:
        for error in errors:
            print(error)

        sys.exit(1)
