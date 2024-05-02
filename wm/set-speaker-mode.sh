#!/bin/bash
set -eu

if [[ $# -eq 0 ]]; then
	printf >&2 'Usage: %s (headphones | tv)\n' "${0##*/}"
	exit 1
fi

mode="$1"
quiet=false

# Determine sink names
headphones_sink=''
television_sink=''

while read -r sink; do
	if [[ $sink = *hdmi* ]]; then
		television_sink="$sink"
	elif [[ $sink = *Scarlett* ]]; then
		headphones_sink="$sink"
	fi
done < <(pactl list sinks | grep 'Name: ' | awk '{print $2}')

if [[ -z $television_sink ]]; then
	notify 'No television sink found.'
	exit 1
elif [[ -z $headphones_sink ]]; then
	notify 'No headphone sink found.'
	exit 1
fi

# Parse arguments
shift
for arg in "$@"; do
	case "$arg" in
		-q)
			quiet=true
			;;
		--quiet)
			quiet=true
			;;
		*)
			printf >&2 'Unknown argument: %s.\n' "$arg"
			exit 1
	esac
done

function notify() {
	if [[ $# -gt 0 ]] && ! "$quiet"; then
		notify-send 'Speaker change' "$@"
	fi
}

function set_sink() {
	pactl set-default-sink "$1"
}

case "$mode" in
	headphones|hp)
		notify 'Setting computer to headphone mode'
		set_sink "$headphones_sink"
		;;
	television|tv)
		notify 'Setting computer to television mode'
		set_sink "$television_sink"
		;;
	*)
		printf >&2 'Unknown speaker setting: %s.\n' "$mode"
		exit 1
esac
