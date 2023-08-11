#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/games/wine/line'
export WINEHOME="$WINEPREFIX"

cd "$WINEHOME/drive_c/users/$USER/AppData/Local/LINE/bin"
wine LineLauncher.exe \
	< /dev/null \
	> /dev/null \
	2> /dev/null
