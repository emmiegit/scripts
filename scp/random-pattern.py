#!/usr/bin/python3

"""
Simple command-line program to generate random numbers fitting a pattern.

All 'X's in the pattern are replaced with a random digit, for instance:

    SCP-XXXX -> SCP-8651

    Project XXX-XXXXXX-X -> Project 175-482658-6

You can also specify an alternate set of characters to choose from, instead
of only digits.
"""

import argparse
import random
import string


DIGITS             = string.digits
ALPHANUMERIC_ALL   = string.digits + string.ascii_letters
ALPHANUMERIC_LOWER = string.digits + string.ascii_lowercase
ALPHANUMERIC_UPPER = string.digits + string.ascii_uppercase

def generate(pattern, replace="X", chars=string.digits):
    return "".join(
        (random.choice(chars) if ch == replace else ch)
        for ch in pattern
    )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Random number pattern replacer")
    argparser.add_argument(
        "-a",
        "--alphanum",
        "--alphanum-lower",
        "--alphanumeric",
        "--alphanumeric-lower",
        dest="chars",
        action="store_const",
        const=ALPHANUMERIC_LOWER,
        default=DIGITS,
        help="Use lowercase alphanumeric as the set of characters",
    )
    argparser.add_argument(
        "-A",
        "--alphanum-upper",
        "--alphanumeric-upper",
        dest="chars",
        action="store_const",
        const=ALPHANUMERIC_UPPER,
        default=DIGITS,
        help="Use uppercase alphanumeric as the set of characters",
    )
    argparser.add_argument(
        "-b",
        "-B",
        "--alphanum-all",
        "--alphanumeric-all",
        dest="chars",
        action="store_const",
        const=ALPHANUMERIC_ALL,
        default=DIGITS,
        help="Use all alphanumeric as the set of characters",
    )
    argparser.add_argument(
        "-c",
        "--characters",
        dest="chars",
        default=DIGITS,
        help="Specify the character set to be used manually",
    )
    argparser.add_argument(
        "-r",
        "--replace",
        "--replace-char",
        dest="replace",
        default="X",
        help="The character to replace with a random selection from the character set"
    )
    argparser.add_argument(
        "pattern",
        nargs="+",
        help="The pattern(s) to have random characters replaced into"
    )

    args = argparser.parse_args()
    results = [generate(pattern, args.replace, args.chars) for pattern in args.pattern]
    print("\n".join(results))
