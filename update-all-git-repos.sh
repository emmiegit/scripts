#!/usr/bin/env bash

[[ $# -gt 0 ]] && cd "$1"

GREEN='\e[32m'
YELLOW='\e[33;1m'
RED='\e[31;1m'
RESET='\e[0m'

for dir in *; do
    [[ ! -d $dir ]] && continue
    cd "$dir"

    RET=0
    REPO=$(basename $(pwd))

    if [[ ! -d .git ]]; then
        printf '[NOT A REPO] %s\n' "$REPO"
        continue
    fi

    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    BASE=$(git merge-base @ @{u})

    if [[ $LOCAL == $REMOTE ]]; then
        printf "[${GREEN}UP-TO-DATE${RESET}] %s\n" "$REPO"
    elif [[ $LOCAL == $BASE ]]; then
        printf "[${YELLOW}NEEDS PULL${RESET}] %s\n" "$REPO"
        git pull --all
        git gc --aggressive
    elif [[ $REMOTE == $BASE ]]; then
        printf "[${YELLOW}NEEDS PUSH${RESET}] %s\n" "$REPO"
        ((RET++))
    else
        printf "[${RED}DIVERGED${RESET}]   %s\n" "$REPO"
        ((RET++))
    fi

    cd ..
done

exit $RET

