#!/usr/bin/env bash

HASH_SCRIPT='/usr/local/scripts/arch/hash-media.py'
LOCATIONS=("${HOME}/Pictures/Anime" "${HOME}/Pictures/Wallpapers")

on_exit() {
    echo 'Done.'
    exit $?
}

on_cancel() {
    echo 'Interrupted by user.'
    exit 1
}

trap on_exit EXIT
trap on_cancel SIGTERM SIGINT

if [[ ! -f $HASH_SCRIPT ]]; then
    echo >&2 'Cannot find hash script.'
    exit 1
fi

for dir in "${LOCATIONS[@]}"; do
    if [[ -d $dir ]]; then
        "$HASH_SCRIPT" "$dir"
    fi
done

