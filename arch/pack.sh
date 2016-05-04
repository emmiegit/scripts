#!/usr/bin/env bash
set -eu

pack() {
    dest="$HOME/Documents/Relic/$1.zip"
    [[ -f "$dest" ]] && mv -f "$dest" "$dest~"
    cd "$2"
    7z a -tzip -mx=2 "$dest" *
    printf 'Archive created at %s composed of files in %s.\n' "$dest" "$2"
    cd - > /dev/null
}

main() {
    pack co.commit  ~/Pictures/Comics/commitstrip
    pack co.dilbert ~/Pictures/Comics/dilbert
    pack co.smbc    ~/Pictures/Comics/smbc
    pack co.xkcd    ~/Pictures/Comics/xkcd
    pack music      ~/Music
    pack osu        /media/media/Games/osu\!/Songs
    read -p 'Finished. '
}

[[ $(basename "$0") == pack.sh ]] && main

