#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/MonsterGirlQuest'
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

if [[ $# -eq 1 ]]; then
	set -eu
	case "$1" in
		rpg|paradox)
			readonly path="Monster Girl Quest Paradox/Game.exe"
			;;
		ng|ng+)
			readonly path="Monster Girl Quest (NG+)/mon_que.exe"
			;;
		1|2|3)
			readonly path="Monster Girl Quest (Part $1)/mon_que.exe"
			;;
	esac

	run "$path"
	set +eu
else
	echo 'Only sourcing variables. Specify which part you want to run the game.'
fi

