#!/bin/bash
set -eu

export WINEARCH='win32'
export WINEPREFIX='/media/media/games/wine/zoo-tycoon-2'
export WINEHOME="$WINEPREFIX"

cd "$WINEPREFIX/drive_c/Program Files/Zoo Tycoon 2 Ultimate Collection"

if [[ $# -gt 0 ]]; then
	if [[ $1 == '-k' ]]; then
		wineserver -k
		exit
	fi
fi

wine autorun.exe \
	< /dev/null \
	> /dev/null \
	2> /dev/null \
	&
disown
