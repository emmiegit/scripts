#!/usr/bin/env bash

[[ $# -gt 0 ]] && cd "$1"

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
        printf '[UP-TO-DATE] %s\n' "$REPO"
    elif [[ $LOCAL == $BASE ]]; then
        printf '[NEEDS PULL] %s\n' "$REPO"
        git pull --all
        git gc --aggressive
    elif [[ $REMOTE == $BASE ]]; then
        printf '[NEEDS PUSH] %s\n' "$REPO"
        ((RET++))
    else
        printf '[DIVERGED]   %s\n' "$REPO"
        ((RET++))
    fi

    cd - > /dev/null
done

exit $RET

