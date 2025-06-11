#!/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

UNMAP = {
    "：": ":",
    "＂": '"',
    "？": "?",
    # TODO |, \
}


def unmap_windows_chars(path):
    new_path = path
    for part, sub in UNMAP.items():
        new_path = new_path.replace(part, sub)
    return new_path if new_path != path else None


class RipDownloader:
    def __init__(self, args):
        self.temp_dir = None
        self.dest_dir = args.destination
        self.youtube_dl_program = args.youtube_downloader
        self.autotagger_script = args.autotagger_script if args.autotag else None
        self.ffmpeg_binary = args.ffmpeg_binary
        self.convert_m4a = args.convert_m4a

    def __enter__(self):
        self.temp_dir = TemporaryDirectory(prefix="rip")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.temp_dir.cleanup()

    def __repr__(self):
        return f"<{type(self).__name__} writing to '{self.temp_dir.name}' at {hex(id(self))}>"

    def download_audio(self, url):
        output = os.path.join(self.temp_dir.name, "%(title)s.%(ext)s")
        command = [self.youtube_dl_program, url, "--no-playlist", "-x", "-o", output]
        print(command)
        subprocess.check_output(command, stdin=subprocess.DEVNULL)

    def process_files(self):
        paths_to_tag = []
        for path in os.listdir(self.temp_dir.name):
            if os.path.isfile(path):
                continue

            # Replace Windows-safe replacement characters, if present
            new_path = unmap_windows_chars(path)
            if new_path is not None:
                old_sourcefile = os.path.join(self.temp_dir.name, path)
                new_sourcefile = os.path.join(self.temp_dir.name, new_path)
                os.rename(old_sourcefile, new_sourcefile)
                print(f"{old_sourcefile} -> {new_sourcefile}")
                path = new_path

            filename, ext = os.path.splitext(path)

            if self.convert_m4a and ext.casefold() == ".m4a":
                new_path = f"{filename}.opus"
                old_sourcefile = os.path.join(self.temp_dir.name, path)
                new_sourcefile = os.path.join(self.temp_dir.name, new_path)
                command = [
                    self.ffmpeg_binary,
                    "-hide_banner",
                    "-i",
                    old_sourcefile,
                    new_sourcefile,
                ]
                print(command)
                subprocess.check_output(command)
                os.remove(old_sourcefile)
                path = new_path

            sourcefile = os.path.join(self.temp_dir.name, path)
            parts = filename.split(" - ")
            match len(parts):
                case 2:
                    # Move to album subdirectory
                    title, album = parts
                    album_dir = os.path.join(self.dest_dir, album)
                    os.makedirs(album_dir, exist_ok=True)
                    print(f"{filename} -> {album_dir}")

                    destfile = os.path.join(album_dir, title + ext)
                    shutil.move(sourcefile, destfile)
                    paths_to_tag.append(destfile)
                case 1:
                    # Single title song, like fusion collabs
                    print(f"{filename} -> {self.dest_dir}")

                    destfile = shutil.move(sourcefile, self.dest_dir)
                    paths_to_tag.append(destfile)
                case _:
                    print(f"Cannot interpret filename: {filename}", file=sys.stderr)
                    shutil.move(sourcefile, self.dest_dir)

        if paths_to_tag and self.autotagger_script is not None:
            command = [self.autotagger_script] + paths_to_tag
            print(command)
            subprocess.check_output(command)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Download assistant for SiIva-style rips",
    )
    argparser.add_argument(
        "-y",
        "--youtube-downloader",
        dest="youtube_downloader",
        default="yt-dlp",
        help="The YouTube downloader program to use",
    )
    argparser.add_argument(
        "-T",
        "--autotagger-script",
        dest="autotagger_script",
        default=os.path.expanduser("~/git/scripts/autotag.py"),
        help="The music autotagger script to use",
    )
    argparser.add_argument(
        "-F",
        "--ffmpeg",
        "--ffmpeg-binary",
        dest="ffmpeg_binary",
        default="ffmpeg",
        help="The ffmpeg binary to use",
    )
    argparser.add_argument(
        "-t",
        "--no-tag",
        "--no-autotag",
        dest="autotag",
        action="store_false",
        help="Disable the autotagger after downloading and placing the rip(s)",
    )
    argparser.add_argument(
        "-M",
        "--no-convert-m4a",
        dest="convert_m4a",
        action="store_false",
        help="Disable the m4a to opus conversion",
    )
    argparser.add_argument(
        "-d",
        "--dest",
        "--destination",
        dest="destination",
        default=".",
        help="Specify an alternate download directory for the rip(s)",
    )
    argparser.add_argument(
        "url",
        nargs="+",
        help="URL(s) of the rip(s) that should be downloaded",
    )
    args = argparser.parse_args()

    with RipDownloader(args) as downloader:
        for url in args.url:
            downloader.download_audio(url)
        downloader.process_files()
