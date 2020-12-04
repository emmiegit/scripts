#!/bin/bash
set -eu

readonly blackbox='█'

if [[ -z $DISPLAY ]]; then
	echo 'No $DISPLAY variable set!'
	exit 1
fi

[[ $# -gt 0 ]] && count="$1" || count=1

awk "BEGIN { while (i++ < $count) printf \"$blackbox\" }"
echo
