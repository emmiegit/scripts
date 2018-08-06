#!/bin/sh
set -eu

name='light-locker'
pidfile="/run/user/$UID/light-locker.pid"
flags=(
	'--lock-on-suspend'
	'--no-late-locking'
	'--idle-hint'
)

if [[ -f $pidfile ]]; then
	kill "$(cat "$pidfile")" || true
fi

"$name" "${flags[@]}" \
	> /dev/null \
	2> /dev/null \
	< /dev/null &
disown

echo "$!" > "$pidfile"
