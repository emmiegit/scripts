#!/bin/bash
set -eu

cd '/media/media/games/steam/steamapps/common/Crypt of the NecroDancer/downloaded_mods/monster-music/music'

if [[ $# -eq 0 ]]; then
	echo "Usage: $0 <artist>"
	echo
	echo "Artist can be one of:"
	echo " + 4"
	echo " + chp"
	echo " - 7"
	echo " - aur"
	echo " - csx"
	echo " - csxxeo"
	echo " - kath"
	echo " - onea"
	echo " - onea_quiet"
	echo " - pt"
	echo " - quiet"
	echo " - sn"
	echo " - xeo"
	echo " - FJ"
	echo " - OCR"
	echo " - SG"
	echo
	echo "Where '+' means it's a full soundtrack,"
	echo "and '-' means it's incomplete."
	exit 1
fi

# Gather arguments
artist="$1"
shift
arguments=("$@")

# Playback functions
play_lobby() {
	file="lobby_${artist}.ogg"

	if [[ -f $file ]]; then
		echo "Playing: Lobby"
		mpv "${arguments[@]}" "$file"
	fi
}

play_floor() {
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
		'')
			variant_descriptor=''
	esac

	file="zone${zone}_${floor}_${artist}${variant}.ogg"

	if [[ -f $file ]]; then
		echo "Playing: ${zone}-${floor} ${variant_descriptor}"
		mpv "${arguments[@]}" "$file"
	fi
}

play_boss() {
	boss="$1"

	case "$boss" in
		1)
			boss_name='King Conga'
			;;
		2)
			boss_name='Death Metal'
			;;
		3)
			boss_name='Deep Blues'
			;;
		4)
			boss_name='Coral Riff'
			;;
		5)
			boss_name='Dead Ringer'
			;;
		6)
			boss_name='Necrodancer'
			;;
		8)
			boss_name='Golden Lute'
			;;
		9)
			boss_name='Fortissimole'
			;;
		11)
			boss_name='The Conductor'
			;;
	esac

	file="boss_${boss}_${artist}.ogg"

	if [[ -f $file ]]; then
		echo "Playing: ${boss_name}"
		mpv "${arguments[@]}" "$file"
	fi
}

# Main
play_lobby

for zone in {1..5}; do
	for floor in {1..3}; do
		if [[ $zone == 3 ]]; then
			play_floor "$zone" "$floor" c
			play_floor "$zone" "$floor" h
		else
			play_floor "$zone" "$floor" ''
		fi
	done

	play_boss "$zone"
done
