#!/bin/env python3

import os
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

YOUTUBE_DL_PROGRAM = "yt-dlp"
AUTOTAGGER_PROGRAM = os.path.expanduser("~/scripts/autotag.py")


def download_audio(directory, url):
    output = os.path.join(directory, "%(title)s.%(ext)s")
    command = [YOUTUBE_DL_PROGRAM, url, "-x", "-o", output]
    print(command)
    subprocess.check_output(command)


def process_files(temp_dir, dest="."):
    paths_to_tag = []
    for path in os.listdir(temp_dir):
        if os.path.isfile(path):
            continue

        filename, ext = os.path.splitext(path)
        parts = filename.split(" - ")
        match len(parts):
            case 2:
                # Move to album subdirectory
                title, album = parts
                album_dir = os.path.join(dest, album)
                os.makedirs(album_dir, exist_ok=True)
                print(f"{filename} -> {album_dir}")

                sourcefile = os.path.join(temp_dir, path)
                destfile = os.path.join(album_dir, title + ext)
                shutil.move(sourcefile, destfile)
                paths_to_tag.append(destfile)
            case 1:
                # Single title song, like fusion collabs
                print(f"{filename} -> {dest}")

                sourcefile = os.path.join(temp_dir, path)
                destfile = shutil.move(path, dest)
                paths_to_tag.append(destfile)
            case _:
                print(f"Cannot interpret filename: {filename}", file=sys.stderr)

    if AUTOTAGGER_PROGRAM is not None:
        command = [AUTOTAGGER_PROGRAM] + paths_to_tag
        print(command)
        subprocess.check_output(command)

if __name__ == "__main__":
    with TemporaryDirectory(prefix="rip") as temp_dir:
        for url in sys.argv[1:]:
            download_audio(temp_dir, url)

        process_files(temp_dir)

