#!/usr/bin/env bash

missing=0

for dep in $@; do
    if pacman -Qs "^$dep$" > /dev/null; then
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

