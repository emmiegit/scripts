#!/bin/sh
set -x

exec sudo \
	ionice -c 3 \
		nice rsync \
		-vrtpAXlHogS \
		--progress \
		--delete-after \
		"$@" -- /media/archive/* "/media/${1:-extern}"

