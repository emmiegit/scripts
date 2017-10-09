#!/bin/sh
set -x

exec sudo \
	ionice -c 3 \
		nice rsync \
		-vrtpAXlHogS \
		--progress \
		--safe-links \
		--delete-after \
		"$@" -- /media/archive/* /media/ExternalDisk

