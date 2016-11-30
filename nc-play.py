#!/usr/bin/env python3
import random
import subprocess
import sys

NORMAL = 0
NIGHTCORE = 1
ANTICORE = 2
RANDOM = -1


def help_and_exit():
    print("Usage: %s [option...] song...")
    print("Options")
    print("  -h, --help                 Print this help message")
    print("  -n, --nightcore-only       Only play at 1.5x speed")
    print("  -a, --anticore-only        Only play at 2/3rds speed")
    print("  -s, --random-speeds        Randomly choose speeds between 0.5 and 1.8")
    print("  -p, --pitch-adjust         Adjust pitch when changing speed")
    exit(0)


def play(songs, modes, pitch_adjust):
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
        "--audio-pitch-correction=%s" % pitch_adjust,
        song,
    ))


if __name__ == '__main__':
    songs = []
    modes = (NORMAL, NIGHTCORE, ANTICORE)
    pitch_adjust = 'no'

    for arg in sys.argv[1:]:
        if arg in ('-h', '--help'):
            help_and_exit()
        elif arg in ('-n', '--nightcore-only'):
            modes = (NIGHTCORE,)
        elif arg in ('-a', '--anticore-only', '--vaporwave'):
            modes = (ANTICORE,)
        elif arg in ('-s', '--random-speeds'):
            modes = (RANDOM,)
        elif arg in ('-p', '--pitch-adjust'):
            pitch_adjust = 'yes'
        else:
            songs.append(arg)

    if not songs:
        print("No songs were specified.")
        exit(1)

    try:
        while True:
            play(songs, modes, pitch_adjust)
    except KeyboardInterrupt:
        exit()

