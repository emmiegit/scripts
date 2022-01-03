#!/bin/bash
set -eu

password="$(pass show computer/titus/borg-raw)"
archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
backup="/media/archive/backup/titus/borg"
locations=(
	"$HOME"
	"/etc"
	"/var"
	"/media/media"
	"/media/archive/git"
)

export BORG_PASSPHRASE="$password"
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
