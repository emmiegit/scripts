#!/bin/bash
set -eu

# Note that the exclude section has videos I have deleted from my local computer,
# but retain on remote in case I wish to rewatch it some time later.

exec \
	ionice -c 3 \
		nice rsync \
			-vahH \
			--progress \
			--exclude=films/Conclave \
			--exclude=films/Flightplan \
			"$@" -- /media/media/videos/{anime,films,television} rsync.net:./videos/
