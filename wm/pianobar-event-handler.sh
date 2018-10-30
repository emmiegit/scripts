#!/bin/sh

cd "$(dirname "$0")"
[ "$1" == "songstart" ] && cat > nowplaying
