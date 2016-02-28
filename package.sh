#!/usr/bin/env bash
set -e

pack() {
    dest=~/Documents/Relic/"$1".zip
    [ -f "$dest" ] && mv -f $dest $dest~
    cd $2
    7z a -tzip -mx=2 "$dest" *
    echo "Archive created at $dest composed of files in $2."
    cd - > /dev/null
}

main() {
    pack wps        ~/Pictures/Wallpapers         &&
    pack co.commit  ~/Pictures/Comics/commitstrip &&
    pack co.dilbert ~/Pictures/Comics/dilbert     &&
    pack co.smbc    ~/Pictures/Comics/smbc        &&
    pack co.xkcd    ~/Pictures/Comics/xkcd        &&
    pack mus        ~/Music                       &&
    printf "Finished. "
    read
}

[[ $(basename $0) == package.sh ]] && main

