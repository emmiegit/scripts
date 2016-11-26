#!/bin/sh
set -eu

if [ "$(cat /etc/hostname)" == "Titus" ]; then
	printf >&2 'Refusing to sync to self.\n'
	exit 1
fi

if [ "$#" -eq 0 ]; then
    printf >&2 'Usage: %s path-to-sync\n' "$0"
    exit 1
fi

docmd() {
	echo "$@"
	"$@"
}

remote=TitusHamachi
source="$(dirname "$1")"
dest="$1"

shift
docmd rsync -vrtzpAXl --safe-links $@ "$remote:$dest" "$source"

