#!/bin/bash
set -eu

export WINEPREFIX=/media/media/games/wine/steam
export WINEHOME="$WINEPREFIX"
export WINEARCH=win32

cd "$WINEPREFIX/drive_c/Program Files/Steam/steamapps/common/Crazy Taxi"
exec wine 'Crazy Taxi.exe'
