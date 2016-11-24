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

REMOTE=TitusHamachi
SOURCE="$(dirname "$1")"
DEST="$1"

rsync -vrtzpAXl --safe-links --delete-after "$REMOTE:$DEST" "$SOURCE"

