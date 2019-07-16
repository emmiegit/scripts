#!/bin/bash
set -euo pipefail

# Based on https://github.com/sasawat/firefox-ctrl-q-workaround

readonly window="$(xdotool getactivewindow)"
readonly name="$(xprop -id "$window" | awk -F '"' '/WM_CLASS/{print $4}')"

case "$name" in
	Firefox) ;;
	Firefox Developer Edition) ;;
	firefoxdeveloperedition) ;;
	*) xvkbd -xsendevent -text "\Cq" ;;
esac
