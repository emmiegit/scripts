#!/bin/bash
set -eu

# Stop old instances
polybar-msg cmd quit

# Launch bars
for bar in "$@"; do
	polybar "$bar" 2>&1 >"/tmp/$USER/polybar-$bar.log" &
done

# Run as daemons
disown
