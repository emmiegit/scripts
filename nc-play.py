#!/usr/bin/env python

import argparse
import math
import random
import subprocess
import sys

NORMAL = 0
NIGHTCORE = 1
ANTICORE = 2
RANDOM = -1


def play(args, mpv_args):
    song = random.choice(args.song)
    speed = random.uniform(args.min_speed, args.max_speed)

    command = ["mpv", "--no-video", f"--speed={speed}"]

    if not args.pitch_adjust:
        command.append("--audio-pitch-correction=no")

    command.extend(mpv_args)
    command.append(song)

    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        exit(1)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        "nc-play",
        description="Automatically play song(s) at random speeds",
    )
    argparser.add_argument(
        "-p",
        "--pitch-adjust",
        action="store_true",
        help="Adjust pitch when changing speed",
    )
    argparser.add_argument(
        "-a",
        "--min",
        "--min-speed",
        dest="min_speed",
        type=float,
        default=0.5,
        help="The minimum speed in range",
    )
    argparser.add_argument(
        "-b",
        "--max",
        "--max-speed",
        dest="max_speed",
        type=float,
        default=1.8,
        help="The maximum speed in range",
    )
    argparser.add_argument("song", nargs="+", help="Which song(s) to play")
    args, mpv_args = argparser.parse_known_args()

    try:
        while True:
            play(args, mpv_args)
    except KeyboardInterrupt:
        exit()
