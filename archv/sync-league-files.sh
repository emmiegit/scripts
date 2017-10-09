#!/bin/sh

src='/media/media/Games/League of Legends/Riot Games'
dest='/media/media/Games/Lutris/league-of-legends/drive_c'

exec ionice -c 3 \
		nice -n 5 \
			rsync \
				-vrtpAXl \
				--progress \
				--safe-links \
				--delete-after \
				"$@" "$src" "$dest"

