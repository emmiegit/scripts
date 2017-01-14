#!/bin/bash
set -eu

if [[ $# -eq 0 ]]; then
	color="$(( (RANDOM % 7) + 1 ))"
else
	color="$1"
fi

own_window=false
args=(
	"-C $color"
	"-Bst"
)

"$own_window" && args+=('-c')

tty-clock -f '%A %B %d, %Y' "${args[@]}"

