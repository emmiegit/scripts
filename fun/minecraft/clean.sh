#!/usr/bin/env bash

if [ -f lock ]; then
    read -p 'Cannot clean while server is running.'
    exit 1
fi

rm -f logs/*

cd world.bak
for item in *; do
    if [[ $item != "old.*" ]]; then
        trash "$item"
    fi
done
cd - > /dev/null

read -p 'Done.'

