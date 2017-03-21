#!/bin/bash
set -eu

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/SayaNoUta'
export WINEHOME="$WINEPREFIX"

if [[ $# -gt 0 ]] && [[ $1 == source ]]; then
	exit
fi

wine "$WINEPREFIX/drive_c/Program Files/SayaNoUta/saya.exe" \
	< /dev/null \
	> /dev/null \
	2>&1 \
	&
disown

