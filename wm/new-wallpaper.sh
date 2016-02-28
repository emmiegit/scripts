#!/usr/bin/env bash

SPREAD=bg-fill              # Strategy for displaying wallpapers. See "man feh".
DIR=~/Pictures/Wallpapers   # Wallpaper directory. Section refers to the subdirectory.
SECTION=

[[ -n $1 ]] && SECTION="$1"

export DISPLAY=:0
feh --recursive --randomize --"$SPREAD" "$DIR/$SECTION"

