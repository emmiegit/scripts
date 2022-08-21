#!/bin/sh
set -eu

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 [mode]" >&2
	exit 1
fi

exec rofi -show "$1" -modi "$1" \
	-font 'mono 12' -columns 3 \
	-disable-history \
	-color-window '#222222, #222222, #b1b4b3' \
	-color-normal '#222222, #b1b4b3, #222222, #005577, #b1b4b3' \
	-color-active '#222222, #b1b4b3, #222222, #007763, #b1b4b3' \
	-color-urgent '#222222, #b1b4b3, #222222, #77003d, #b1b4b3' \
	-kb-row-select 'Tab' -kb-row-tab ''
