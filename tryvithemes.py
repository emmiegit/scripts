#!/usr/bin/env python
from __future__ import with_statement
from glob import glob
import os, subprocess

THEME_PATHS = (
    "/usr/share/vim/vim74/colors",
    os.path.expanduser("~/.vim/colors"),
)

SAMPLES = '/usr/local/scripts/dat/samples/*'

if __name__ == "__main__":
    theme_fn = subprocess.check_output(["mktemp", "/tmp/vim-themes-XXXXXXX.txt"])
    themes = set()

    for path in THEME_PATHS:
        for dirname, dirs, files in os.walk(path):
            for fn in files:
                if fn.lower().endswith(".vim"):
                    themes.add(fn[:-4])

    themes = list(themes)
    themes.sort()

    with open(theme_fn, 'w+') as fh:
        fh.write("\n".join(themes))

    commands = ["vim", "-p", theme_fn]
    subprocess.call(commands + glob(SAMPLES))

    os.remove(fn)

