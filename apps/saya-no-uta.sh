#!/bin/bash

export WINEARCH='win32'
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/SayaNoUta'
export WINEHOME="$WINEPREFIX"

if [[ $# -gt 0 ]] && [[ $1 == exec ]]; then
	set -eu

	LC_ALL='ja_JP.UTF-8' \
		wine "$WINEPREFIX/drive_c/Program Files/NitroPlus/SayaNoUta/saya.exe" \
			< /dev/null \
			> /dev/null \
			2>&1 \
			&
	disown

	set +eu
else
	echo "No 'exec' argument given, sourcing variables only."
fi

