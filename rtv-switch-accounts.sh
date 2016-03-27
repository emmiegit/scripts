#!/usr/bin/env bash

get_rtv_dir() {
    if [[ -n $XDG_CONFIG_HOME ]]; then
        RTV_DIR="$XDG_CONFIG_HOME/rtv"
    else
        RTV_DIR="$HOME/.config/rtv"
    fi

    if [[ ! -d $RTV_DIR ]]; then
        printf >&2 'Cannot find rtv config directory.\n'
        exit 1
    fi

    echo "$RTV_DIR"
}

main() {
    cd "$(get_rtv_dir)" || return 1

    printf 'Available accounts:\n'
    local accounts=()
    local index=0
    for acct in *.token; do
        accounts+=("$acct")
        printf '%d: %s\n' "$index" "${acct:0:-6}"
        ((index++))
    done

    read -rp 'Enter a number to switch to: ' choice

    if [[ "$((choice))" != "$choice" ]]; then
        echo >&2 "Invalid index: $choice"
        exit 1
    fi

    acct=${accounts[${choice}]}

    if [[ -z $acct ]]; then
        echo >&2 "Invalid index: $choice"
        exit 1
    fi

    rm -f refresh-token
    ln "$acct" refresh-token
    printf 'Switched rtv account to %s.\n' "${acct:0:-6}"
}

main

