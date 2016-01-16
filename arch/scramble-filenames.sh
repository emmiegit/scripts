#!/bin/bash
set -e

[[ $# -gt 0 ]] && cd $@
salt=$RANDOM

hashnm() {
    echo "$1$salt" | sha256sum | cut -c 1-64 | rev
}

for fn in *; do
    [[ ! -f $fn ]] && continue
    [[ $fn == files.txt ]] && continue
    newfn=$(hashnm "$fn")
    echo "$fn -> $newfn" >> files.txt
    mv "$fn" "$newfn"
done

