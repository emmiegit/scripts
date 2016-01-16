#!/usr/bin/env bash

missing=0

# Uses pacman -Q instead of pacman -Qs because the latter does not allow
# searching by exact package name. It is slower, but oh well.
for dep in $@; do
    if pacman -Q | grep -q "^$dep"; then
        printf "$dep: \e[32m\e[1mok\e[0m\n"
    else
        printf "$dep: \e[31m\e[1mfail\e[0m\n"
        ((missing++))
    fi
done

if [[ $missing -eq 0 ]]; then
    printf 'All dependencies met.\n'
else
    printf 'Not all dependencies are installed.\n'
    exit $missing
fi

