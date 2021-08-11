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

readonly remote=Titus
readonly source="$(dirname "$1")"
readonly dest="$1"

shift
docmd rsync -vahHAXP -zz --safe-links --delete-after "$@" "$remote:$dest" "$source"
