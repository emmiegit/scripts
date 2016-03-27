#!/usr/bin/env bash

RED="\e[31m\e[1m"
GREEN="\e[32m"
RESET="\e[0m"
missing=0

for dep in "$@"; do
    if pacman -Qs "^$dep$" > /dev/null; then
        printf "%s: ${GREEN}ok${RESET}\n" "$dep"
    else
        printf "%s: ${RED}fail${RESET}\n" "$dep"
        ((missing++))
    fi
done

if [[ $missing -eq 0 ]]; then
    printf 'All dependencies met.\n'
else
    printf 'Not all dependencies are installed.\n'
    exit $missing
fi

