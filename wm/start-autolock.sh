#!/bin/sh
LOCKER='/usr/local/scripts/wm/lock.sh'
SUSPEND=false
SUSPEND_CMD='systemctl suspend'

if $SUSPEND; then
    xautolock -resetsaver -detectsleep -time 5 -locker "${LOCKER}" -killtime 30 -killer "${SUSPEND_CMD}" &
else
    xautolock -resetsaver -detectsleep -time 5 -locker "${LOCKER}" &
fi
disown

