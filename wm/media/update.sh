#!/bin/sh

# Settings
full=false

while getopts ':f' opt; do
	case "$opt" in
		f)
			full=true
			;;
		:)
			printf >&2 "Option %s requires an argument\n" "$OPTARG"
			exit 1
			;;
		\?)
			printf >&2 "Invalid argument: '-%s'\n" "$OPTARG"
			exit 1
			;;
	esac
done
shift "$((OPTIND - 1))"

# Run mpd command
source "${0%/*}/mpc.sh"

if "$full"; then
	mpc rescan
else
	mpc update --wait
fi
