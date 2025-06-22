#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

IMG_MOVE_PROGRAM = "sha224mv"
ALLOWED_EXTENSIONS = (
    "bmp",
    "gif",
    "jpg",
    "jpeg",
    "png",
)
EXTENSION_MAPPING = {"jpeg": "jpg"}


class ImageMover:
    def __init__(
        self, ignore_extensions: bool, remap_extensions: bool, dry_run: bool
    ) -> None:
        self.ignore_extensions = ignore_extensions
        self.remap_extensions = remap_extensions
        self.dry_run = dry_run

    def rename_files(self, paths: list[str]) -> int:
        new_paths = []
        for path in paths:
            new_path = self.remap_and_mark(path)
            if new_path is not None:
                new_paths.append(new_path)

        return subprocess.run([IMG_MOVE_PROGRAM] + new_paths).returncode

    def remap_and_mark(self, filename: str) -> str | None:
        if not os.path.isfile(filename):
            return None

        file_stem, extension = os.path.splitext(filename)
        extension = extension.removeprefix(".")

        if not self.ignore_extensions:
            if extension not in ALLOWED_EXTENSIONS:
                return None

        if self.remap_extensions:
            try:
                new_extension = EXTENSION_MAPPING[extension]
            except KeyError:
                new_extension = None

        if self.dry_run:
            # TODO add --dry-run to hash-digest-rename
            print(f"+ {filename}")
            return None
        elif new_extension is not None:
            os.rename(filename, f"{file_stem}.{new_extension}")
            return f"{file_stem}.{new_extension}"
        else:
            return f"{file_stem}.{extension}"


if __name__ == "__main__":
    argparser = argparse.ArgumentParser("igmv")
    argparser.add_argument(
        "file",
        nargs="*",
        help="Files to operate on. In the absence of any arguments, runs on the current directory.",
    )
    argparser.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        help="Operate even on files outside the allowed extension list.",
    )
    argparser.add_argument(
        "-r",
        "--no-remap-extension",
        dest="remap_extensions",
        action="store_false",
        help="Don't remap extensions when renaming files.",
    )
    argparser.add_argument(
        "-n",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Don't actually perform any actions.",
    )
    args = argparser.parse_args()

    mover = ImageMover(args.force, args.remap_extensions, args.dry_run)
    paths = args.file if args.file else os.listdir(".")
    status_code = mover.rename_files(paths)
    sys.exit(status_code)
