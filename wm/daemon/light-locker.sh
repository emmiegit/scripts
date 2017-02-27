#!/bin/sh
set -eu

name='light-locker'
flags=(
	'--lock-on-suspend'
)

pkill "\^$name\$" || true
"$name" "${flags[@]}" \
	> /dev/null \
	2> /dev/null \
	< /dev/null &
disown

