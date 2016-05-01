#!/usr/bin/env bash

OSU_SONG_DIR='/media/media/Games/osu!/Songs'

main() {
    local songs=()
    cd "$OSU_SONG_DIR"

    for dir in *; do
        if [[ -d $dir ]] && [[ $dir != Failed ]]; then
            songs+=("$dir")
        fi
    done

    [[ -f 'songs.txt' ]] && cp -f songs.txt songs.txt.old
    printf '%s\n' "${songs[@]}" > songs.txt
}

[[ $# -eq 0 ]] \
    && main \
    || main $@

