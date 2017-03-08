#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/MonsterGirlQuest'
export WINEHOME="$WINEPREFIX"

if [[ $# -eq 1 ]]; then
	set -eu
	LC_ALL='ja_JP.UTF-8' \
		wine "$WINEPREFIX/drive_c/Program Files/Monster Girl Quest (Part $1)/mon_que.exe" \
			< /dev/null \
			> /dev/null \
			2>&1 \
			&
	disown
else
	echo 'Only sourcing variables. Specify which part you want to run the game.'
fi
