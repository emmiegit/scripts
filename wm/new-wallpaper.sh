#!/usr/bin/env bash
set -eu

# Strategy for displaying wallpapers. See "man feh".
SPREAD=bg-center

# Wallpaper directory.
DIR=~/Pictures/Wallpapers/all

# The wallpaper subdirectory.
SECTION="$(cat /usr/local/scripts/dat/wallpaper_section)"

[[ $# -gt 0 ]] && SECTION="$1"
${DISPLAY+"false"} && export DISPLAY=:0

feh --recursive --randomize --"$SPREAD" "$DIR/$SECTION"

