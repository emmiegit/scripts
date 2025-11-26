#!/bin/bash
set -eu

case "$(cat /etc/hostname)" in
	Titus)
		workspaces=({1..4})
		;;
	Augustus)
		workspaces=({1..5} 7)
		;;
	*)
		notify-msg "Unknown hostname $(cat /etc/hostname), cannot determine workspaces to restore"
		exit 1
esac

for workspace in "${workspaces[@]}"; do
	i3-resurrect restore --workspace "$workspace"
done
