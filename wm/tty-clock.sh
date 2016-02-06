#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    COLOR="$((($RANDOM % 7) + 1))"
else
    COLOR="$1"
fi

OWN_WINDOW=false
ARGS="-C $COLOR"

$OWN_WINDOW && ARGS+=" -cn"

tty-clock -f '%A %B %d, %Y' -st $ARGS

