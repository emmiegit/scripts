#!/bin/bash
set -eu

source "${0%/*}/borg-source.sh"

archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
locations=(
	"$HOME"
	"/etc"
	"/var"
	"/media/media"
	"/media/archive/git"
)

exec \
	ionice -c 3 \
	nice -n 10 \
		borg create \
			-v \
			--stats \
			--progress \
			--compression auto,lzma \
			"$backup::$archive" \
			"${locations[@]}"
