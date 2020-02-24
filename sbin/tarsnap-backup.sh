#!/bin/bash
set -eu

archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
locations=()

for argument in "$@"; do
	case "$argument" in
		root)
			locations+=(
				"$HOME"
				"/etc"
				"/var"
			)
			;;
		archive)
			locations+=('/media/archive/git')
			;;
		media)
			locations+=('/media/media')
			;;
		*)
			echo "Unknown location specifier: $1"
			exit 1
	esac
done

exec \
	ionice -c 3 \
	nice -n 10 \
		tarsnap -c \
		-f "$archive-$1" \
		-v \
		--print-stats \
		"${locations[@]}" \
		> /var/log/tarsnap.log \
		2>&1
