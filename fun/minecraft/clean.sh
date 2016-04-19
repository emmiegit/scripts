#!/usr/bin/env bash
set -eu

if [[ -f lock ]]; then
    read -p 'Cannot clean while server is running.'
    exit 1
fi

rm -f logs/*

cd backups
for item in *; do
    [[ -d $item ]] && 7z a old.7z "$item"
done
cd - > /dev/null

read -p 'Done.'

