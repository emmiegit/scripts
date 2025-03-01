#!/usr/bin/env python

import argparse
import random


def generate_bingo_variant(word, hole, probability):
    return "".join(hole if random.random() < probability else c for c in word)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-c",
        "--count",
        default=1,
        type=int,
        help="Number of iterations to produce",
    )
    argparser.add_argument(
        "-w",
        "--word",
        default="BINGO",
        help="An alternate string to substitute",
    )
    argparser.add_argument(
        "-x",
        "--hole-character",
        default=" ",
        help="An alternate character for holes",
    )
    argparser.add_argument(
        "-p",
        "--hole-probability",
        default=0.5,
        type=float,
        help="What the probability of holes in the string is",
    )
    args = argparser.parse_args()

    for _ in range(args.count):
        print(generate_bingo_variant(args.word, args.hole_character, args.hole_probability))
