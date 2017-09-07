#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/Wine/MonsterGirlQuest'
export WINEHOME="$WINEPREFIX"

run() {
	LC_ALL='ja_JP.UTF-8' \
		wine "$WINEPREFIX/drive_c/Program Files/$1" \
			< /dev/null \
			> /dev/null \
			2> /dev/null \
			&
	disown
}

if [[ $# -gt 1 ]]; then
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
		*)
			printf "Unknown part: %s\n", "$1"
			exit 1
			;;
	esac

	run "$path"
	set +eu
else
	echo 'Only sourcing variables. Specify which part you want to run the game.'
fi

