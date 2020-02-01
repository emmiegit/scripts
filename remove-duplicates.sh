#!/bin/bash
set -eu

locations=(
	"$HOME/pictures/anime"
	"$HOME/pictures/comics/ben-garrison"
	"$HOME/pictures/comics/clay-bennett"
	"$HOME/pictures/comics/smbc"
	"$HOME/pictures/comics/star-tribune-sack"
	"$HOME/pictures/comics/trump"
	"$HOME/pictures/games/Civ V/Miscellaenous Screenshots/"
	"$HOME/pictures/miscellaneous/4chan"
	"$HOME/pictures/miscellaneous/doujinshi"
	"$HOME/pictures/miscellaneous/ken-m"
	"$HOME/pictures/miscellaneous/poland-ball"
	"$HOME/pictures/miscellaneous/redraw-reigen"
	"$HOME/pictures/miscellaneous/unnamed"
	"$HOME/pictures/movies"
	"$HOME/pictures/photographs/Pets"
	"$HOME/pictures/scp/memes"
	"$HOME/pictures/wallpapers/desktop"
	"$HOME/pictures/wallpapers/phone"
)

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
