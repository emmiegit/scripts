#!/bin/bash
set -eu

source "$(dirname "$0")/dat/media-dirs"

hash_new() {
	/usr/local/scripts/archv/darch.sh -m "$1"
}

hash_old() {
	/usr/local/scripts/archv/media-hash.py "$1"
}

hasher=hash_old

if [[ $# -gt 0 ]]; then
	for arg in "$@"; do
		case "$arg" in
			new)
				echo "Using new hash program."
				hasher=hash_new
				;;
			*)
				echo >&2 "Unknown argument: $arg"
				exit 1
				;;
		esac
	done
fi

for dir in "${locations[@]}"; do
	echo "Hashing $dir..."
	"$hasher" "$dir"
	echo
done
