#!/bin/bash
set -eu

cd '/media/media/games/steam/steamapps/common/Crypt of the NecroDancer/downloaded_mods/monster-music/music'

if [[ $# -eq 0 ]]; then
	echo "Usage: $0 <artist>"
	echo
	echo "Artist can be one of:"
	echo " + 4"
	echo " + chp"
	echo " - kath"
	echo " - csx"
	echo " - csxxeo"
	echo " - sn"
	echo " - SG"
	echo " - XEO"
	echo " - quiet"
	echo " - 7"
	echo " - FJ"
	echo " - OCR"
	echo
	echo "Where '+' means it's a full soundtrack,"
	echo "and '-' means it's incomplete."
	exit 1
fi

# Gather arguments
artist="$1"
shift
arguments=("$@")

play() {
	zone="$1"
	floor="$2"
	variant="$3"

	case "$variant" in
		c)
			variant_descriptor='Cold'
			;;
		h)
			variant_descriptor='Hot'
			;;
	esac

	file="zone${zone}_${floor}_${artist}${variant}.ogg"

	if [[ -f $file ]]; then
		echo "Playing: ${zone}-${floor} ${variant_descriptor}"
		mpv "${arguments[@]}" "$file"
	fi
}

for zone in {1..5}; do
	for floor in {1..3}; do
		if [[ $zone == 3 ]]; then
			play "$zone" "$floor" c
			play "$zone" "$floor" h
		else
			play "$zone" "$floor" ''
		fi
	done
done
