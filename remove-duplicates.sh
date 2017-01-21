#!/bin/bash

hash_script='/usr/local/scripts/archv/media-hash.py'
locations=(
	"${HOME}/Pictures/Anime"
	"${HOME}/Pictures/Games/Civ V/Miscellaenous Screenshots/"
	"${HOME}/Pictures/Misc/Ben Garrison"
	"${HOME}/Pictures/Misc/Redraw Reigen"
	"${HOME}/Pictures/Photographs/Pets"
	"${HOME}/Pictures/Comics/smbc"
	"${HOME}/Pictures/Wallpapers/desktop"
	"${HOME}/Pictures/Wallpapers/phone")

on_exit() {
    printf "\nDone.\n"
    exit $?
}

on_cancel() {
    echo "\nInterrupted by user.\n"
    exit 1
}

trap on_exit EXIT
trap on_cancel SIGTERM SIGINT

if [[ ! -f $hash_script ]]; then
    echo >&2 'Cannot find hash script.'
    exit 1
fi

"$hash_script" "${locations[@]}" "$@"

