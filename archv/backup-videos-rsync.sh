#!/bin/bash
set -eu

exec \
	ionice -c 3 \
		nice rsync \
			-vahH \
			--progress \
			"$@" -- /media/media/videos/{anime,films,television} rsync.net:./videos/
