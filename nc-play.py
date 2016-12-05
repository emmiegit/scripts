#!/usr/bin/env python3
import math
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
    print("      --min=[value]          Set the minimum speed when choosing randomly")
    print("      --max=[value]          Set the maximum speed")
    print("      --flags=[value]        Give mpv additional flags")
    exit(0)


def play(songs, options):
    song = random.choice(songs)
    mode = random.choice(options['modes'])

    if mode == NORMAL:
        speed = 1
    elif mode == NIGHTCORE:
        speed = 1.5
    elif mode == ANTICORE:
        speed = 0.67
    elif mode == RANDOM:
        speed = random.random() * (options['max_speed'] - options['min_speed']) + options['min_speed']

    flags = [
        "mpv",
        "--no-video",
        "--speed=%f" % speed,
    ]

    if not options['pitch_adjust']:
        flags.append("--audio-pitch-correction=no")

    if options['extra_flags']:
        flags += options['extra_flags']

    flags.append(song)
    subprocess.run(flags)


if __name__ == '__main__':
    songs = []
    options = {
            'modes': (NORMAL, NIGHTCORE, ANTICORE),
            'pitch_adjust': False,
            'extra_flags': [],
            'min_speed': 0.5,
            'max_speed': 1.8,
    }

    for arg in sys.argv[1:]:
        if arg in ('-h', '--help'):
            help_and_exit()
        elif arg in ('-n', '--nightcore-only'):
            options['modes'] = (NIGHTCORE,)
        elif arg in ('-a', '--anticore-only', '--vaporwave'):
            options['modes'] = (ANTICORE,)
        elif arg in ('-s', '--random-speeds'):
            options['modes'] = (RANDOM,)
        elif arg in ('-p', '--pitch-adjust'):
            options['pitch_adjust'] = True
        elif arg.startswith('--min='):
            try:
                options['min_speed'] = float(arg[6:])
            except ValueError:
                print("Not a floating point number: %s" % arg[6:])
                exit(1)
        elif arg.startswith('--max='):
            try:
                options['max_speed'] = float(arg[6:])
            except ValueError:
                print("Not a floating point number: %s" % arg[6:])
                exit(1)
        elif arg.startswith('--flags='):
            options['extra_flags'] = arg[8:].split(' ')
        elif arg.startswith('-'):
            print("Not a recognized option: %s" % arg)
            exit(1)
        else:
            songs.append(arg)

    if not songs:
        print("No songs were specified.")
        exit(1)

    if not math.isfinite(options['min_speed']) or not math.isfinite(options['max_speed']):
        print("Speeds must be real numbers.")
        exit(1)

    if options['min_speed'] < 0 or options['max_speed'] < 0:
        print("Speeds must be positive.")
        exit(1)

    if options['min_speed'] > options['max_speed']:
        print("Minimum speed is larger than the maximum.")
        exit(1)

    try:
        while True:
            play(songs, options)
    except KeyboardInterrupt:
        exit()

