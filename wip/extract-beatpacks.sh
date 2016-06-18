#!/usr/bin/env bash
set -e

OSU_SONG_DIR='/opt/osu/game/Songs'

# A script to unpack osu! beatmap packs.
# Requires: dtrx, trash
# If you don't want to install those dependencies, replace
# 'trash' with 'rm' and 'dtrx' with the proper call to 7z, tar, gunzip, etc.

main() {
	if [[ "*.rar" != '*.rar' ]]; then
		echo 'Extracting beatmap packs...'
		dtrx -fv *.rar

		echo 'Removing beatmap packs...'
		trash *.rar
	fi

	if [[ "*.osz" != '*.osz' ]]; then
		echo 'Extracting osz files...'
		dtrx -v *.osz

		echo 'Moving beatmaps...'
		for beatmap in *.osz; do
			beatmap="${beatmap:0:-4}"
			if [[ ! -d "$OSU_SONG_DIR/$beatmap" ]]; then
				mv -v "$beatmap" "$OSU_SONG_DIR"
			else
				echo "Directory already exists, skipping $beatmap..."
			fi
		done

		echo 'Removing osz files...'
		trash *.osz
	fi
}

[[ $# -gt 0 ]] && cd "$1"
main

