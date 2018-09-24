#!/bin/bash
set -euo pipefail

export WINEPREFIX=/media/media/games/wine/league-of-legends
export WINEHOME="$WINEPREFIX"
export WINEARCH=win32

exec wine 'C:\Riot Games\League of Legends\LeagueClient.exe' >/tmp/league-output-$EUID.log 2>&1
