#!/bin/sh
SUSPEND=false

if $SUSPEND; then
    xautolock -resetsaver -detectsleep -time 5 -locker '/usr/local/scripts/wm/lock.sh' -killtime 30 -killer 'sudo pm-suspend' &
else
    xautolock -resetsaver -detectsleep -time 5 -locker '/usr/local/scripts/wm/lock.sh' &
fi
disown

