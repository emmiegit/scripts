#!/usr/bin/env python
from __future__ import with_statement
from glob import glob
import os, subprocess, tempfile

THEME_PATHS = (
    "/usr/share/vim/vim74/colors",
    os.path.expanduser("~/.vim/colors"),
)

SAMPLES = '/usr/local/scripts/dat/samples/*'

if __name__ == "__main__":
    temp_fh = tempfile.NamedTemporaryFile(mode="w+")
    themes = set()

    for path in THEME_PATHS:
        if os.path.isdir(path):
            for dirname, dirs, files in os.walk(path):
                for fn in files:
                    if fn.lower().endswith(".vim"):
                        themes.add(fn[:-4])

    themes = list(themes)
    themes.sort()

    temp_fh.write("\n".join(themes))
    temp_fh.flush()
    commands = ["vim", "-p", temp_fh.name]
    subprocess.call(commands + glob(SAMPLES))
    temp_fh.close()

