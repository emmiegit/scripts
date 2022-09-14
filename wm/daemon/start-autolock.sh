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

readonly locker='/usr/local/scripts/wm/lock'
readonly runkill=false
readonly killer_cmd="$(cat '/usr/local/scripts/dat/autolock_killer_cmd')"
readonly delay_time="$(cat '/usr/local/scripts/dat/autolock_delay')"

pkill xautolock || true

if "$runkill"; then
	xautolock -resetsaver -detectsleep -time "$delay_time" -locker "$locker" -killtime 30 -killer "$killer_cmd" &
else
	xautolock -resetsaver -detectsleep -time "$delay_time" -locker "$locker" &
fi
disown

if [[ $? -ne 0 ]]; then
	echo >&2 'Autolock program exited with nonzero status code.'
	notify-send 'Autolock program exited with nonzero status code.'
	exit 1
fi
