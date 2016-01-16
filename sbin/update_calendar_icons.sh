#!/usr/bin/env bash
set -e

quit_nautilus=false
colors="blue purple red"
today=`date +%d`

[[ $EUID != 0 ]] && echo "You might need to be root to run this command."

cd /usr/share/icons/Numix-Circle/scalable/apps
for color in $colors; do
    symlink_name="calendar-$color-today.svg"
    file_name="calendar-$color-$today.svg"
    [ -L "$symlink_name" ] && rm "$symlink_name"
    ln -s "$file_name" "$symlink_name"
done

cd /usr/share/icons/Numix/256/places
symlink_name="calendar-today.svg"
file_name="calendar-$today.svg"
[ -L "$symlink_name" ] && rm "$symlink_name"
ln -s "$file_name" "$symlink_name"

$quit_nautilus && nautilus -q

