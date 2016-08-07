#!/usr/bin/env bash

HASH_SCRIPT='/usr/local/scripts/arch/media-hash.py'
LOCATIONS=("${HOME}/Pictures/Anime" "${HOME}/Pictures/Pets" "${HOME}/Pictures/Comics/smbc" "${HOME}/Pictures/Wallpapers/desktop" "${HOME}/Pictures/Wallpapers/phone")

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

