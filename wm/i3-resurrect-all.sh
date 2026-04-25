#!/bin/bash
set -eu

case "$(hostname)" in
	Titus)
		workspaces=({1..4})
		;;
	Augustus)
		workspaces=({1..5})
		;;
	*)
		notify-send "Unknown hostname $(hostname), cannot determine workspaces to restore"
		exit 1
esac

for workspace in "${workspaces[@]}"; do
	i3-resurrect restore --workspace "$workspace"
	sleep 0.2  # give time for the windows to appear in
done
