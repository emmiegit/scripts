#!/bin/sh
set -x

readonly backup_dir="/media/${1:-extern}"

if [[ ! -d $backup_dir ]]; then
	echo >&2 "No such directory: $backup_dir"
	exit 1
fi

exec sudo \
	ionice -c 3 \
		nice rsync \
		-vrtpAXlHogS \
		--progress \
		--delete-before \
		--exclude=temporary/ \
		"$@" -- /media/archive/* "$backup_dir"
