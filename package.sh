#!/usr/bin/env bash

pack() {
    dest=$3/"$1".rar
    [[ -f $dest ]] && mv -f $dest $dest~
    cd $2
    rar a -v -t -m5 $dest *
    echo "Archive created at $dest composed of files in $2."
    cd - > /dev/null
}

pack wallpapers ~/Pictures/Wallpapers /tmp/
# etc...
read

