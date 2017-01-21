#!/bin/sh
set -eu

/usr/local/scripts/wm/vi-keyswap.sh
mkdir -m700 -p "/tmp/$USER/"{vim_undo,pacaur,cache}

