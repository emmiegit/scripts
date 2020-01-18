#!/bin/bash
set -eu

archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
locations=()

case "$1" in
	root)
		locations+=(
			"$HOME"
			"/etc"
			"/var"
		)
		;;
	archive)
		locations+=('/media/archive')
		;;
	media)
		locations+=('/media/media')
		;;
	*)
		echo "Unknown location specifier: $1"
		exit 1
esac

set -x
exec \
	ionice -c 3 \
	nice -n 10 \
		tarsnap -c \
		-f "$archive-$1" \
		-v \
		--print-stats \
		"${locations[@]}"
