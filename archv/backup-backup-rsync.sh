#!/bin/bash
set -eu

exec \
	ionice -c 3 \
		nice rsync \
			-vahH \
			--progress \
			--delete-after \
			--exclude=lost+found \
			--exclude=backup/luks-headers \
			--exclude=temporary \
			"$@" -- /media/archive/* rsync.net:./backup/
