#!/usr/bin/env python

import os
import shlex

FEHBG_PATH = os.path.expanduser("~/.fehbg")
WALLPAPER_COUNT = 3


def parse_fehbg_args(line: str, wallpaper_count: int) -> list[str]:
    # Example: feh --no-fehbg --bg-fill /some/file /another/file
    args = shlex.split(line)

    # Skip the first argument, the feh binary
    for index in range(1, len(args)):
        if not args[index].startswith("-"):
            break

    # All the arguments are options
    if index == len(args) - 1 and args[index].startswith("-"):
        return []

    # index now has the first non-argument path
    return args[index : index + wallpaper_count]


def parse_fehbg(path: str, wallpaper_count: int) -> list[str]:
    with open(FEHBG_PATH) as file:
        for line in file:
            if not line.startswith("#!"):
                return parse_fehbg_args(line, wallpaper_count)
    raise ValueError(f"No matching feh line in {path}")


if __name__ == "__main__":
    wallpapers = parse_fehbg(FEHBG_PATH, WALLPAPER_COUNT)
    for wallpaper in wallpapers:
        print(wallpaper)
