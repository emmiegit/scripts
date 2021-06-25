#!/bin/bash
set -eu

[[ $EUID == 0 ]] && exec sudo -u emmie "$0"
[[ -z $DISPLAY ]] && DISPLAY=:0

if [[ $# -eq 0 ]]; then
	printf >&2 'Usage: %s (draw | osu)\n' "$(basename "$0")"
	exit 1
fi

mode="$1"
tablet_part='Wacom Intuos S 2 Pen stylus'
quiet=false

shift
for arg in "$@"; do
	case "$arg" in
		-q)
			quiet=true
			;;
		--quiet)
			quiet=true
			;;
		*)
			printf >&2 'Unknown argument: %s.\n' "$arg"
			exit 1
	esac
done

function notify() {
	if ! "$quiet"; then
		notify-send "$@"
	fi
}

function main() {
	case "$(hostname)" in
		Titus)
			# 1920 x 1200
			case "$mode" in
				draw)
					notify 'Setting tablet to drawing mode.'
					xsetwacom --set "$tablet_part" MapToOutput 'HEAD-0'
					xsetwacom --set "$tablet_part" Area 0 0 14796 8250
					;;
				osu)
					notify 'Setting tablet to circle-clicking mode.'
					xsetwacom --set "$tablet_part" MapToOutput 'HEAD-0'
					xsetwacom --set "$tablet_part" Area 2000 2000 8220 5500
					;;
				*)
					printf >&2 'Unknown tablet mode: %s.\n' "$mode"
					exit 1
					;;
			esac
			;;
		Domitian)
			# 1440 x 900
			case "$mode" in
				draw)
					notify 'Setting tablet to drawing mode.'
					xsetwacom --set "$tablet_part" MapToOutput 'LVDS-1'
					;;
				osu)
					notify 'Setting tablet to circle-clicking mode.'
					xsetwacom --set "$tablet_part" MapToOutput 'LVDS-1'
					xsetwacom --set "$tablet_part" Area 2000 2000 8000 5750
					;;
				*)
					printf >&2 'Unknown tablet mode: %s.\n' "$mode"
					exit 1
			esac
			;;
		*)
			printf >&2 'Unknown tablet mode: %s.\n' "$mode"
			exit 1
			;;
	esac
}

main

