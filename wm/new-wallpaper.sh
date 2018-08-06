#!/bin/bash
set -eu

# Strategy for displaying wallpapers. See "man feh".
SPREAD=bg-fill

# Wallpaper directory.
DIR="$HOME/pictures/wallpapers/desktop"

# The wallpaper subdirectory.
SECTION="$(cat '/usr/local/scripts/dat/wallpaper_section')"

[[ $# -gt 0 ]] && SECTION="$1"

if [[ ${DISPLAY:-none} == none ]]; then
	export DISPLAY=':0'
fi

feh --recursive --randomize --"$SPREAD" "$DIR/$SECTION"

