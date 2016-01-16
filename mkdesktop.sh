#!/usr/bin/env bash

case $# in
0)
    printf "Enter the name of the desktop file: "
    read fn
    dest=~/Desktop
    ;;
1)
    fn=$1
    dest=~/Desktop
    ;;
2)
    fn=$1
    dest=$2
    ;;
*)
    echo "Usage: $(basename $0) [desktop-file-name] [destination-dir]"
    exit 1
    ;;
esac

# Determine the user's default choice of editor
if [ "x$VISUAL" == "x" ]; then
    if [ "x$EDITOR" == "x" ]; then
        EDITOR=vi
    fi
else
    EDITOR=$VISUAL
fi

dest="${dest}/${fn}.desktop"
cp "$(dirname $0)/dat/template.desktop" "$dest"
#chmod 755 "$dest" # Only for *buntu systems
"$EDITOR" "$dest"

