#!/bin/bash
set -eu

exec \
	ionice -c 3 \
		nice rsync \
			-vahH \
			--progress \
			--exclude=*.on_rsync \
			"$@" -- /media/media/videos/{anime,films,television} rsync.net:./videos/
