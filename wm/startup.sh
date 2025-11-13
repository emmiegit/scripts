#!/bin/sh
set -eu

mkdir -p "/tmp/$USER/"{aur,cache,private,vim_undo}
ln -sf "/tmp/$USER/aur" "$HOME/.cache/yay"

/usr/local/scripts/wm/vi-keyswap.sh
/usr/local/scripts/wm/reset-repeat-rate.sh
/usr/local/scripts/wm/screenlayout/run.sh
/usr/local/scripts/wm/set-speaker-mode.sh headphones
