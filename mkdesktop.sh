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

[ -z "$EDITOR" ] && EDITOR=vi

dest=$dest/$fn\.desktop
echo "\
[Desktop Entry]
Version=1.0
Name=
Comment=
Exec=
Icon=
Terminal=false
Categories=Utility;Application;" > $dest
chmod 755 $dest
$EDITOR $dest

