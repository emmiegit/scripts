#!/bin/sh
set -eu

# SSD health checker for the Samsung 850 EVO. Be sure to research your particular
# model to look for the correct attribute name, and obviously the right device too.
DEVICE='/dev/sdc'

get_health() {
	sudo smartctl -a "$DEVICE" | grep 'Wear_Leveling_Count' | awk '{print $4}'
}

printf 'Check health of device "%s"? [Y/n] ' "$DEVICE"

read -r response
case "$response" in
	n*)
		printf 'Not checking device.\n'
		exit 1
		;;
	N*)
		printf 'Not checking device.\n'
		exit 1
		;;
esac

printf 'Life remaining for "%s": %s%%\n' "$DEVICE" "$(get_health | perl -pe 'chomp')"

