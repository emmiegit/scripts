#!/bin/bash
set -euo pipefail

# Based on https://github.com/sasawat/firefox-ctrl-q-workaround

readonly window="$(xdotool getactivewindow)"
readonly name="$(xprop -id "$window" | awk -F '"' '/WM_CLASS/{print $4}')"

if [[ $name != 'Firefox' ]] && [[ $name != 'Firefox Developer Edition' ]]; then
	xvkbd -xsendevent -text "\Cq"
fi
