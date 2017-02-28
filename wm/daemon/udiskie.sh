#!/bin/sh
set -eu

name='udiskie'
flags=(
	'--notify'
)

trap : SIGHUP

pkill -HUP "$name" || true
"$name" "${flags[@]}" \
	> /dev/null \
	2> /dev/null \
	< /dev/null &
disown

