#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/MonsterGirlQuest'
export WINEHOME="$WINEPREFIX"

if [[ $# -eq 1 ]]; then
	set -eu
	if [[ $1 == ng ]]; then
		readonly part='NG+'
	else
		readonly part="Part $1"
	fi

	LC_ALL='ja_JP.UTF-8' \
		wine "$WINEPREFIX/drive_c/Program Files/Monster Girl Quest ($part)/mon_que.exe" \
			< /dev/null \
			> /dev/null \
			2>&1 \
			&
	disown

	unset part
	set +eu
else
	echo 'Only sourcing variables. Specify which part you want to run the game.'
fi

