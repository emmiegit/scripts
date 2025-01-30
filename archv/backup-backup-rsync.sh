#!/bin/bash
set -eu

exec \
	ionice -c 3 \
		nice rsync \
			-vahH \
			--progress \
			--preallocate \
			--delete-after \
			--exclude=temporary/ \
			"$@" -- /media/archive/* rsync.net:./backup/
