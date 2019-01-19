#!/bin/bash
set -euo pipefail

export WINEPREFIX=/media/media/games/wine/league-of-legends
export WINEHOME="$WINEPREFIX"
export WINEARCH=win32
export MESA_GL_VERSION_OVERRIDE=4.5COMPAT
export MESA_GLTHREAD=TRUE
export VBLANK_MODE=0

exec wine 'C:\Riot Games\League of Legends\LeagueClient.exe' >/tmp/league-output-$EUID.log 2>&1
