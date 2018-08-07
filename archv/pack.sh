#!/bin/bash
set -eu

pack() {
	dest="$HOME/documents/relic/$1.zip"
	[[ -f "$dest" ]] && mv -f "$dest" "$dest~"
	cd "$2"
	7z a -tzip -mx=2 "$dest" *
	printf 'Archive created at %s composed of files in %s.\n' "$dest" "$2"
	cd - > /dev/null
}

main() {
	pack co.commit	~/pictures/comics/commitstrip
	pack co.dilbert ~/pictures/comics/dilbert
	pack co.smbc	~/pictures/comics/smbc
	pack co.xkcd	~/pictures/comics/xkcd
	pack music		~/music
	pack osu		/media/media/Games/osu\!/Songs
	read -p 'Finished. '
}

[[ $(basename "$0") == pack.sh ]] && main

