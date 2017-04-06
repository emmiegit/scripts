#!/bin/bash
set -eu

locations=(
	"$HOME/Pictures/Anime"
	"$HOME/Pictures/Games/Civ V/Miscellaenous Screenshots/"
	"$HOME/Pictures/Misc/Ben Garrison"
	"$HOME/Pictures/Misc/Redraw Reigen"
	"$HOME/Pictures/Misc/Unnamed"
	"$HOME/Pictures/Photographs/Pets"
	"$HOME/Pictures/Comics/smbc"
	"$HOME/Pictures/Comics/misc"
	"$HOME/Pictures/Wallpapers/desktop"
	"$HOME/Pictures/Wallpapers/phone")

hash_new() {
	/usr/local/scripts/archv/darch.sh -m "$1"
}

hash_old() {
	/usr/local/scripts/archv/media-hash.py "$1"
}

hasher=hash_new

if [[ $# -gt 0 ]]; then
	for arg in "$@"; do
		case "$arg" in
			old)
				echo "Using old hash program."
				hasher=hash_old
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

