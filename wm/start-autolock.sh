#!/bin/sh
LOCKER='/usr/local/scripts/wm/lock.sh'
KILL=false
KILLER_CMD="$(cat '/usr/local/scripts/dat/autolock_killer_cmd')"
DELAY_TIME="$(cat '/usr/local/scripts/dat/autolock_delay')"

if $KILL; then
    xautolock -resetsaver -detectsleep -time "${DELAY_TIME}" -locker "${LOCKER}" -killtime 30 -killer "${KILLER_CMD}" &
else
    xautolock -resetsaver -detectsleep -time "${DELAY_TIME}" -locker "${LOCKER}" &
fi
disown

