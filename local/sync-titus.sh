#!/bin/bash
set -eu

if [[ -f /etc/hostname ]]; then
	if [[ "$(cat /etc/hostname)" == "Titus" ]]; then
		printf >&2 'Refusing to sync to self.\n'
		exit 1
	fi
fi

if [[ "$#" -eq 0 ]]; then
	printf >&2 'Usage: %s path-to-sync\n' "$0"
	exit 1
fi

docmd() {
	echo "$@"
	"$@"
}

remote=Titus

if [[ $# -eq 1 ]]; then
	source="$1"
	dest="$(dirname "$1")"
	shift
else
	source="$1"
	dest="$2"
	shift 2
fi

docmd rsync -vahHP -zz --safe-links --delete-after "$@" "$remote:$source" "$dest"
