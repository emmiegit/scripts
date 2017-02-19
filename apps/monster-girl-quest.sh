#!/bin/bash
set -eu

export WINEARCH=win32
export WINEPREFIX='/media/media/Games/PlayOnLinux/wineprefix/MonsterGirlQuest'
[[ $# -eq 1 ]] && wine "$WINEPREFIX/drive_c/Program Files/Monster Girl Quest $1/mon_que.exe"

