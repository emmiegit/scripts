#!/bin/bash
set -eu

if [[ ! -f /usr/local/scripts/wm/lock-screen-sleep.sh ]]; then
	echo >&2 'Cannot find lock script.'
	notify-send 'Cannot find lock script.'
	exit 1
elif [[ ! -f /usr/local/scripts/dat/autolock_killer_cmd ]]; then
	echo >&2 'Cannot find autolock killer command.'
	notify-send 'Cannot find autolock killer command.'
	exit 1
elif [[ ! -f /usr/local/scripts/dat/autolock_delay ]]; then
	echo >&2 'Cannot find autolock delay time.'
	notify-send 'Cannot find autolock delay time.'
	exit 1
fi

LOCKER='/usr/local/scripts/wm/lock.sh'
KILL=false
KILLER_CMD="$(cat '/usr/local/scripts/dat/autolock_killer_cmd')"
DELAY_TIME="$(cat '/usr/local/scripts/dat/autolock_delay')"

pkill xautolock || true
if "$KILL"; then
	xautolock -resetsaver -detectsleep -time "${DELAY_TIME}" -locker "${LOCKER}" -killtime 30 -killer "${KILLER_CMD}" &
else
	xautolock -resetsaver -detectsleep -time "${DELAY_TIME}" -locker "${LOCKER}" &
fi
disown

if [[ $? -ne 0 ]]; then
	echo >&2 'Autolock program exited with nonzero status code.'
	notify-send 'Autolock program exited with nonzero status code.'
	exit 1
fi

