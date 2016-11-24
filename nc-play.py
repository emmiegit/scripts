#!/usr/bin/env python3
import random
import subprocess
import sys

NORMAL = 0
NIGHTCORE = 1
ANTICORE = 2
RANDOM = -1


def play(songs, modes):
    song = random.choice(songs)
    mode = random.choice(modes)

    if mode == NORMAL:
        speed = 1
    elif mode == NIGHTCORE:
        speed = 1.5
    elif mode == ANTICORE:
        speed = 0.67
    elif mode == RANDOM:
        # 0.5 to 1.8
        speed = random.random() * 1.3 + 0.5

    subprocess.run((
        "mpv",
        "--no-video",
        "--speed=%f" % speed,
        "--audio-pitch-correction=no",
        song,
    ))


if __name__ == '__main__':
    songs = []
    modes = (NORMAL, NIGHTCORE, ANTICORE)

    for arg in sys.argv[1:]:
        if arg in ('-h', '--help'):
            help_and_exit()
        elif arg in ('-a', '--anticore-only', '--vaporwave'):
            modes = (ANTICORE,)
        elif arg in ('-n', '--nightcore-only'):
            modes = (NIGHTCORE,)
        elif arg in ('-s', '--random-speeds'):
            modes = (RANDOM,)
        else:
            songs.append(arg)

    if not songs:
        print("No songs were specified.")
        exit(1)

    try:
        while True:
            play(songs, modes)
    except KeyboardInterrupt:
        exit()

