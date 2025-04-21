#!/bin/bash
set -eu

exec \
	ionice -c 3 \
		nice rsync \
			-vahH \
			--progress \
			--delete-after \
			--exclude=temporary/ \
			"$@" -- /media/media/videos/{anime,films,television} rsync.net:./videos/

