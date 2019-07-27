#!/bin/bash
set -euo pipefail

# Based on https://github.com/sasawat/firefox-ctrl-q-workaround

readonly window="$(xdotool getactivewindow)"
readonly name="$(xprop -id "$window" | awk -F '"' '/WM_CLASS/ { print $4 }')"

readonly blacklist=(
	'Firefox'
	'Firefox Developer Edition'
	'firefoxdeveloperedition'
)

for item in "${blacklist[@]}"; do
	[[ $name == $item ]] && exit
done

xvkbd -xsendevent -text "\Cq"
