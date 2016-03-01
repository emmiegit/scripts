#!/bin/sh
set -e

OSU_SONG_DIR='/opt/osu/game/Songs'

# A script to unpack osu! beatmap packs.
# Requires: dtrx

[ $# -gt 0 ] && cd "$1"

echo 'Extracting beatmap packs...'
dtrx -f *.rar

echo 'Removing beatmap packs...'
rm *.rar

echo 'Extracting osz files...'
dtrx *.osz

echo 'Moving beatmaps...'
for beatmap in *; do
    if [ -d "$beatmap" ]; then
        mv "$beatmap" "$OSU_SONG_DIR"
    else
        echo "Skipping $beatmap..."
    fi
done

echo 'Removing osz files...'
rm *.osz


