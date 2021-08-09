#!/bin/sh
set -eu

ln -sf "/tmp/$USER/aur" "$HOME/.cache/yay"

/usr/local/scripts/wm/screenlayout/run.sh
