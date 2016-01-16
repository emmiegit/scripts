#!/usr/bin/env bash

argno=1

for arg in $@; do
    printf '%d: <%s>\n' "$argno" "$arg"
    ((argno++))
done

