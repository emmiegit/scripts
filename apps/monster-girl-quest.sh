#!/bin/bash
set -eu

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/MonsterGirlQuest'
export WINEHOME="$WINEPREFIX"

if [[ $# -eq 1 ]]; then
	set -eu
	if [[ $1 == ng ]]; then
		readonly local part='NG+'
	else
		readonly local part="Part $1"
	fi

	LC_ALL='ja_JP.UTF-8' \
		wine "$WINEPREFIX/drive_c/Program Files/Monster Girl Quest ($part)/mon_que.exe" \
			< /dev/null \
			> /dev/null \
			2>&1 \
			&
	disown
else
	echo 'Only sourcing variables. Specify which part you want to run the game.'
fi

