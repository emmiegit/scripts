#!/usr/bin/env bash

SPREAD=bg-fill              # Strategy for displaying wallpapers. See "man feh".
DIR=~/Pictures/Wallpapers   # Wallpaper directory. Section refers to the subdirectory.
SECTION=

export DISPLAY=:0
feh --recursive --randomize --"$SPREAD" "$DIR/$SECTION"

