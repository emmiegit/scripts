#!/usr/bin/env bash

[[ $# -gt 0 ]] && cd "$1"

GREEN='\e[32m'
YELLOW='\e[33;1m'
BOLD_RED='\e[31;1m'
RED='\e[31m'
BLUE='\e[34m'
RESET='\e[0m'

check_repo() {
    local LOCAL=$(git rev-parse @)
    local REMOTE=$(git rev-parse @{u})
    local BASE=$(git merge-base @ @{u})

    if [[ $LOCAL == $REMOTE ]]; then
        printf "[${GREEN}UP-TO-DATE${RESET}]${CHANGES} %s\n" "$REPO"
    elif [[ $LOCAL == $BASE ]]; then
        printf "[${YELLOW}NEEDS PULL${RESET}]${CHANGES} %s\n" "$REPO"
        git pull --all
        git gc --aggressive
    elif [[ $REMOTE == $BASE ]]; then
        printf "[${YELLOW}NEEDS PUSH${RESET}]${CHANGES} %s\n" "$REPO"
        return 1
    else
        printf "[${BOLD_RED}DIVERGED${RESET}]${CHANGES}   %s\n" "$REPO"
        return 1
    fi
}

main() {
    local UNTRACKED=false
    local TO_COMMIT=false
    local RET=0
    local lines=()

    for dir in *; do
        [[ ! -d $dir ]] && continue
        cd "$dir"
        REPO=$(basename $(pwd))
        if [[ ! -d .git ]]; then
            printf '[NOT A REPO] %s\n' "$REPO"
            continue
        fi

        if git status | grep -Eq '(Untracked files|Changes not staged for commit)'; then
            CHANGES="${RED}!${RESET}"
            UNTRACKED=true
        elif git status | grep -q 'Changes to be committed'; then
            CHANGES="${BLUE}!${RESET}"
            TO_COMMIT=true
        else
            CHANGES=' '
        fi

        lines+=("$(check_repo)")
        [ $? -gt 0 ] && ((RET++))

        cd ..
    done

    $UNTRACKED && printf "'${RED}!${RESET}' means that untracked or unstaged files are present.\n"
    $TO_COMMIT && printf "'${BLUE}!${RESET}' means that changes have been added but not commited.\n"
    printf "%s\n" "${lines[@]}"
    return $RET
}

main

