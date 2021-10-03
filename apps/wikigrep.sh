#!/bin/bash
set -eu

cd "$HOME/git/wikidot-css-extractor"
exec ./grep.py "$@"
