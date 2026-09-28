#!/usr/bin/env python

import argparse
from urllib.parse import quote, unquote


if __name__ == "__main__":
    argparser = argparse.ArgumentParser("percent-quote")
    argparser.add_argument(
        "-d",
        "--decode",
        action="store_true",
        help="Run in decoder mode",
    )
    argparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force encoding of all non-alphanumeric characters",
    )
    argparser.add_argument(
        "input",
        nargs="+",
        help="String inputs to encode/decode",
    )
    args = argparser.parse_args()

    for string in args.input:
        print(quote(string))
