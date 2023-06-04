#!/usr/bin/env python3

"""
Auto-tags songs based on their placement in my directory hierarchy.

Uses the "id3lib" command-line tool, install the id3lib package to get it.

My structure is rooted at my music directory, and from there each top-level directory
is the name of the artist. For instance:

~/music
├── Alice and Bob
│   ├── Negotiating a session key.opus
│   ├── I'm leaving you for Eve.mp3
│   └── Close connection.mp3
└── John Cage
    └── 4′33″.opus

In this structure, "Close connection.mp3" would have an Artist field of "Alice and Bob" and
a Title field of "Close connection".

Occasionally, songs will have a third layer, where they designate the album that they're in.
To go back to an example:

~/music
└── Kawai Sprite
    └── Friday Night Funkin'
        └── Ugh.opus

The file "Ugh.opus" would have an Artist of "Kawai Sprite", a Title of "Ugh", and an
Album field with "Friday Night Funkin'".
(I don't play the game I just like this one song, don't DM me.)

So it's not quite so simple as "artist is the directory you're in".

Because I don't store music outside of my ~/music directory, we will consider this the root,
and any files outside of it or in an unexpected location will yield errors. The music root
can be set via command-line argument.

I get the music directory from the XDG_MUSIC_DIR environment variable, if it exists, or the
field of the same name in ~/.config/user-dirs.dirs, as the FreeDesktop standard enables.
However I don't want to parse it myself so I just call "xdg-user-dir MUSIC" to parse it for me.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

HOME_DIR = os.path.expanduser("~")
NUMBERED_TRACK_REGEX = re.compile(r"(\d+)\. (.+)")

AudioMetadata = namedtuple("AudioMetadata", ("artist", "album", "title", "track"))


def default_music_dir():
    value = os.getenv("XDG_MUSIC_DIR")
    if value is not None:
        return value

    output = subprocess.check_output(["xdg-user-dir", "MUSIC"])
    music_dir = output.strip().decode("utf-8")
    if music_dir != HOME_DIR:
        # Check it wasn't unset
        return music_dir

    return os.path.expanduser("~/music")


def is_subdir(parent, child):
    parent = Path(os.path.realpath(parent))
    child = Path(os.path.realpath(child))
    return parent in child.parents


def get_relative_path(root, path):
    root = os.path.realpath(root)
    path = os.path.realpath(path)
    return Path(os.path.relpath(path, root))


def edit_tags(path, metadata):
    arguments = ["id3tag", "--v1tag"]

    if metadata.artist is not None:
        arguments.append(f"--artist={metadata.artist}")

    if metadata.album is not None:
        arguments.append(f"--album={metadata.album}")

    if metadata.title is not None:
        arguments.append(f"--song={metadata.title}")

    if metadata.track is not None:
        arguments.append(f"--track={metadata.track}")

    arguments.append("--")
    arguments.append(path)
    print(" ".join(arguments))
    subprocess.check_call(arguments)


def interpret_title(basename):
    stem, _ = os.path.splitext(basename)
    match = NUMBERED_TRACK_REGEX.fullmatch(stem)
    if match is None:
        return stem, None
    else:
        return match[2], match[1]


def interpret_path(path):
    match path.parts:
        case (basename,):
            title, track = interpret_title(basename)
            return AudioMetadata(
                title=title,
                track=track,
                artist=None,
                album=None,
            )
        case (artist, basename):
            title, track = interpret_title(basename)
            return AudioMetadata(
                title=title,
                track=track,
                artist=artist,
                album=None,
            )
        case (artist, album, basename):
            title, track = interpret_title(basename)
            return AudioMetadata(
                title=title,
                track=track,
                artist=artist,
                album=album,
            )
        case _:
            raise ValueError(f"Path '{path}' too deep")


def process_file(orig_path, args):
    root = args.music_dir

    if not is_subdir(root, orig_path):
        raise ValueError(f"Path '{orig_path}' not within music directory")

    if not os.path.isfile(orig_path):
        raise ValueError(f"Not regular file: {orig_path}")

    path = get_relative_path(root, orig_path)
    metadata = interpret_path(path)
    edit_tags(orig_path, metadata)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Auto-tagger for music files")
    argparser.add_argument(
        "-m",
        "--music-dir",
        "--music-root",
        dest="music_dir",
        default=default_music_dir(),
        help="Override the directory to use as the music root",
    )
    argparser.add_argument(
        "FILE",
        nargs="+",
        help="All files to process",
    )
    args = argparser.parse_args()
    print(f"Using music path: {args.music_dir}")

    exit_status = 0
    for path in args.FILE:
        try:
            process_file(path, args)
        except Exception as error:
            print(error, file=sys.stderr)
            exit_status += 1
    sys.exit(exit_status)
