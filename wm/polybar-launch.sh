#!/bin/bash
set -eu

# Stop old instances
if compgen -G /tmp/polybar_mqueue.*; then
	polybar-msg cmd quit
fi

# Load mpd password
export MPD_PASSWORD="$(cat "$HOME/.mpd/password.txt")"

# Launch bars
for bar in "$@"; do
	polybar "$bar" 2>&1 >"/tmp/$USER/polybar-$bar.log" &
done

# Run as daemons
disown
