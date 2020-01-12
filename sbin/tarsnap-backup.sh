#!/bin/bash
set -eu

archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
locations=(
	"$HOME"
	"/etc"
	"/var"
	"/media/media"
	"/media/archive"
)

exec \
	ionice -c 3 \
	nice -n 10 \
		tarsnap -c \
		-f "$archive" \
		-v \
		--print-stats \
		"${locations[@]}"
