#!/bin/bash

osu_song_dir='/media/media/games/osu!/Songs'

main() {
	local songs=()
	cd "$osu_song_dir"

	for dir in *; do
		if [[ -d $dir ]] && [[ $dir != Failed ]]; then
			songs+=("$dir")
		fi
	done

	[[ -f songs.txt ]] && cp -f songs.txt songs.txt.old
	printf '%s\n' "${songs[@]}" > songs.txt
}

[[ $# -eq 0 ]] \
	&& main \
	|| main "$@"
