#!/usr/bin/env python3
from __future__ import with_statement
from glob import glob
import os
import subprocess
import tarfile
import tempfile

THEME_PATHS = (
    "/usr/share/vim/vim74/colors",
    os.path.expanduser("~/.vim/colors"),
)

SAMPLE_ARCHIVE = "/usr/local/scripts/dat/samples.tar.gz"
SAMPLE_DIR_NAME = "samples"
THEME_LIST_NAME = "themes.txt"

if __name__ == "__main__":
    themes = set()

    for path in THEME_PATHS:
        if os.path.isdir(path):
            for dirname, dirs, files in os.walk(path):
                for fn in files:
                    if fn.lower().endswith(".vim"):
                        themes.add(fn[:-4])

    themes = list(themes)
    themes.sort()

    with tempfile.TemporaryDirectory(prefix="vim_themes_") as temp_dir:
        os.chdir(temp_dir)
        os.mkdir(SAMPLE_DIR_NAME)

        with open(THEME_LIST_NAME, "w") as fh:
            fh.write("\n".join(themes))

        with tarfile.open(SAMPLE_ARCHIVE, "r") as tar_fh:
            names = tar_fh.getnames()

            for name in names:
                if name.startswith("/") or name.startswith(".."):
                    print("Skipping %s, unsafe file name." % name)
                    continue

                tar_fh.extract(name, path=SAMPLE_DIR_NAME)

        commands = ["vim", "-p", THEME_LIST_NAME]
        subprocess.call(commands + glob(os.path.join(SAMPLE_DIR_NAME, "*")))

