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

# Because there are issues with encoding non-ASCII information in a way that mpd can understand
# (it seems to be using latin-1 or something? I can't tell what the issue is), the tool should
# refuse to encode non-ASCII characters as a precaution.
PERMIT_NON_ASCII = False

AudioMetadata = namedtuple("AudioMetadata", ("artist", "album", "title", "track"))
AudioMetadataOverrides = namedtuple("AudioMetadataOverrides", ("artist", "album", "title", "track", "comment", "description", "date", "genre"))


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


def get_override(metadata, overrides, attr):
    primary = getattr(metadata, attr)
    override = getattr(overrides, attr)

    # If override is an empty string, then the caller
    # explicitly wants this field excluded.
    if override == "":
        return None

    return override or primary


def edit_tags(path, metadata, overrides, version=2):
    arguments = ["id3tag", f"--v{version}tag"]

    artist = get_override(metadata, overrides, "artist")
    if artist is not None:
        arguments.append(f"--artist={artist}")

    album = get_override(metadata, overrides, "album")
    if album is not None:
        arguments.append(f"--album={album}")

    title = get_override(metadata, overrides, "title")
    if title is not None:
        arguments.append(f"--song={title}")

    track = get_override(metadata, overrides, "track")
    if track is not None:
        arguments.append(f"--track={track}")

    comment = overrides.comment
    if comment is not None:
        arguments.append(f"--comment={comment}")

    description = overrides.description
    if description is not None:
        arguments.append(f"--desc={description}")

    date = overrides.date
    if date is not None:
        arguments.append(f"--year={date}")

    genre = overrides.genre
    if genre is not None:
        arguments.append(f"--genre={genre}")

    arguments.append("--")
    arguments.append(path)
    cmdline = " ".join(arguments)

    if not PERMIT_NON_ASCII:
        if not all(arg.isascii() and arg.isprintable() for arg in arguments):
            print(f"Command-line contains non-ASCII arguments, denying due to encoding issues:\n    {cmdline}")
            sys.exit(1)

    print(cmdline)
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

    if os.path.islink(orig_path):
        print(f"Warning! {orig_path} is a symlink.")

    overrides = AudioMetadataOverrides(
        artist=args.artist_override,
        album=args.album_override,
        title=args.title_override,
        track=args.track_override,
        comment=args.comment_override,
        description=args.description_override,
        date=args.date_override,
        genre=args.genre_override,
    )

    path = get_relative_path(root, orig_path)
    metadata = interpret_path(path)
    edit_tags(orig_path, metadata, overrides, args.version)


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
        "-1",
        "--v1",
        dest="version",
        action="store_const",
        const=1,
        default=2,
        help="Force use of version 1 for ID tagging",
    )
    argparser.add_argument(
        "-2",
        "--v2",
        dest="version",
        action="store_const",
        const=2,
        help="Force use of version 1 for ID tagging",
    )
    argparser.add_argument(
        "-a",
        "--artist",
        dest="artist_override",
        help="Override the artist value to write for all songs",
    )
    argparser.add_argument(
        "-A",
        "--album",
        dest="album_override",
        help="Override the album value to write for all songs",
    )
    argparser.add_argument(
        "-t",
        "--title",
        dest="title_override",
        help="Override the title value to write for all songs",
    )
    argparser.add_argument(
        "-n",
        "--track",
        dest="track_override",
        help="Override the track value to write for all songs",
    )
    argparser.add_argument(
        "-c",
        "--comment",
        dest="comment_override",
        help="Override the comment value to write for all songs",
    )
    argparser.add_argument(
        "-C",
        "--description",
        dest="description_override",
        help="Override the description value to write for all songs",
    )
    argparser.add_argument(
        "-d",
        "--date",
        "--year",
        dest="date_override",
        help="Override the date value to write for all songs",
    )
    argparser.add_argument(
        "-g",
        "--genre",
        dest="genre_override",
        help="Override the genre value to write for all songs",
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
