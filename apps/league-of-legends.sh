#!/bin/bash
set -euo pipefail

export PATH=/opt/wine-lol/bin
export WINEPREFIX=/media/media/games/wine/league-of-legends
export WINEHOME="$WINEPREFIX"
export WINEARCH=win32
export MESA_GL_VERSION_OVERRIDE=4.5COMPAT
export MESA_GLTHREAD=TRUE
export VBLANK_MODE=0

output="/tmp/league-output-$EUID.log"

while getopts :dk opt; do
	case "$opt" in
		d)
			output="/dev/stdout"
			;;
		k)
			wineserver -k
			exit 0
			;;
		\?)
			echo "Invalid arg: -$OPTARG" >&2
			exit 1
			;;
	esac
done

exec /opt/wine-lol/bin/wine 'C:\Riot Games\League of Legends\LeagueClient.exe' >"$output" 2>&1
