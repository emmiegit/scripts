#!/bin/sh
LOCKER='/usr/local/scripts/wm/lock.sh'
KILL=true
KILLER_CMD="$(cat '/usr/local/scripts/dat/autolock_killer_cmd')"

if $KILL; then
    xautolock -resetsaver -detectsleep -time 5 -locker "${LOCKER}" -killtime 30 -killer "${KILLER_CMD}" &
else
    xautolock -resetsaver -detectsleep -time 5 -locker "${LOCKER}" &
fi
disown

