#!/bin/bash
set -eu

# Strategy for displaying wallpapers. See "man feh".
spread=bg-fill

# Wallpaper directory.
dir="$HOME/pictures/wallpapers/desktop"

# The wallpaper subdirectory.
section="$(cat '/usr/local/scripts/dat/wallpaper_section')"

[[ $# -gt 0 ]] && section="$1"

if [[ ${DISPLAY:-none} == none ]]; then
	export DISPLAY=':0'
fi

feh --recursive --randomize --"$spread" "$dir/$section"

