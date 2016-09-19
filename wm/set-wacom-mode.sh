#!/bin/bash
set -eu

[[ $EUID == 0 ]] && exec sudo -u ammon "$0"
[[ -z $DISPLAY ]] && DISPLAY=:0

if [[ $# -eq 0 ]]; then
    printf >&2 'Usage: %s (draw | osu)\n' "$(basename "$0")"
    exit 1
fi

TABLET_PART_ID='Wacom Intuos S 2 Pen stylus'

case "$(hostname)" in
	Titus)
		# 1920 x 1200
		case "$1" in
			draw)
				notify-send 'Setting tablet to drawing mode.'
				xsetwacom --set "$TABLET_PART_ID" MapToOutput 'HEAD-0'
				;;
			osu)
				notify-send 'Setting tablet to circle-clicking mode.'
				xsetwacom --set "$TABLET_PART_ID" Area 2000 2000 8220 5500
				;;
			*)
				printf >&2 'Unknown tablet mode: %s.\n' "$1"
				exit 1
				;;
		esac
		;;
	Domitian)
		# 1440 x 900
		case "$1" in
			draw)
				notify-send 'Setting tablet to drawing mode.'
				xsetwacom --set "$TABLET_PART_ID" MapToOutput 'LVDS-1'
				;;
			osu)
				notify-send 'Setting tablet to circle-clicking mode.'
				xsetwacom --set "$TABLET_PART_ID" Area 2000 2000 8000 5750
				;;
			*)
				printf >&2 'Unknown tablet mode: %s.\n' "$1"
				exit 1
		esac
		;;
	*)
        printf >&2 'Unknown tablet mode: %s.\n' "$1"
        exit 1
        ;;
esac

