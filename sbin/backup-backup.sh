#!/bin/sh
set -x

readonly backup_dir="/media/${1:-extern}"
shift

if [[ ! -d $backup_dir ]]; then
	echo >&2 "No such directory: $backup_dir"
	exit 1
fi

echo /media/archive "$backup_dir"

exec sudo \
	ionice -c 3 \
		nice rsync \
		-vrtpAXlHogS \
		--progress \
		--preallocate \
		--delete-during \
		--exclude=temporary/ \
		"$@" -- /media/archive/* "$backup_dir"
