#!/usr/bin/env bash
set -eu

[[ $EUID == 0 ]] && exec sudo -u ammon "$0"
[[ -z $DISPLAY ]] && export DISPLAY=:0

if [[ $# -eq 0 ]]; then
    printf >&2 'Usage: %s (draw | osu)\n' "$(basename "$0")"
    exit 1
fi

case "$1" in
    draw)
        notify-send 'Setting tablet to drawing mode.'
        xsetwacom --set 'Wacom Intuos S 2 Pen stylus' MapToOutput HEAD-0
        ;;
    osu)
        notify-send 'Setting tablet to circle-clicking mode.'
        xsetwacom --set 'Wacom Intuos S 2 Pen stylus' Area 2000 2000 8220 5500
        ;;
    *)
        printf >&2 'Unknown tablet mode: %s.\n' "$1"
        exit 1
        ;;
esac

