#!/bin/bash

export WINEPREFIX='/media/media/games/wine/line'
export WINEHOME="$WINEPREFIX"
export WINEARCH=win64

cd "$WINEHOME/drive_c/Program Files/Image-Line/FL Studio 2024/"

case $1 in
	exit|quit|kill|stop)
		wineserver -k
		exit 0
		;;
esac

wine FL64.exe \
	< /dev/null \
	> /dev/null \
	2>&1
