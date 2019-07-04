#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/games/wine/monster-girl-quest'
export WINEHOME="$WINEPREFIX"

run() {
	readonly full_path="$WINEPREFIX/drive_c/Program Files/$1"
	cd "${full_path%/*}"
	LC_ALL='ja_JP.UTF-8' \
		wine "${1##*/}"
			< /dev/null \
			> /dev/null \
			2> /dev/null \
			&
	disown
}

if [[ $# -gt 0 ]]; then
	set -eu
	case "$1" in
		rpg|paradox)
			case "$2" in
				1|2|3)
					readonly path="Monster Girl Quest Paradox (Part $2)/Game.exe"
					;;
				*)
					printf "Unknown part: %s\n", "$2"
					exit 1
					;;
			esac
			;;
		ng|ng+)
			readonly path="Monster Girl Quest (NG+)/mon_que_ng+.exe"
			;;
		1|2|3)
			readonly path="Monster Girl Quest (Part $1)/mon_que.exe"
			;;
		1080|hd|remaster|remastered|upscale|upscaled)
			readonly path="Monster Girl Quest (1080 Upscale)/Monster Girl Quest Remastered.exe"
			;;
		*)
			printf "Unknown part: %s\n", "$1"
			exit 1
			;;
	esac

	run "$path"
else
	echo 'Only sourcing variables. Specify which part you want to run the game.'
fi
