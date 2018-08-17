#!/bin/bash
set -eu

password="$(cat ~/documents/secure/files/borg-passwd.txt)"
archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
backup="/media/archive/backup/titus/borg"
locations=(
	"$HOME"
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
