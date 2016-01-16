#!/usr/bin/env bash

OWN_WINDOW=false
ARGS="-C $(($RANDOM % 8))"

$OWN_WINDOW && ARGS+=" -cn"

tty-clock -f '%A %B %d, %Y' -st $ARGS

