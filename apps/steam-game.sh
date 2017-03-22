#!/bin/bash
set -eu

if [[ $# -eq 0 ]]; then
    printf >&2 'Usage: %s [steam-game-id]\n' "$0"
    exit 1
fi

steam "steam://rungameid/$1" \
	> /dev/null \
	< /dev/null \
	2>&1 &
disown

