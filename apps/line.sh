#!/bin/bash

export WINEPREFIX='/media/media/games/wine/line'
export WINEHOME="$WINEPREFIX"

cd "$WINEHOME/drive_c/users/$USER/AppData/Local/LINE/bin"

case $1 in
	exit|quit|kill)
		wineserver -k
		exit 0
		;;
esac

wine LineLauncher.exe \
	< /dev/null \
	> /dev/null \
	2>&1
