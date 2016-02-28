#!/usr/bin/env bash
set -e

DEST=~/Documents/Relic
HASH_SCRIPT=~/Scripts/arch/hash-media.py
PASSWD=~/Scripts/dat/archpasswd
CLEAR_RECENT=false
TEST_ARCHIVE=false
_remove_lock=true

on_sigterm() {
    echo "Caught user interrupt, closing down."
    if [[ -f $LOCK ]] && $_remove_lock; then
        rm -f $LOCK
    else
        echo "Warning: can't remove lock file."
    fi
    exit 1
}

on_exit() {
    echo "Finished."
    if [[ -f $LOCK ]] && $_remove_lock; then
        rm -f $LOCK
    else
        echo "Warning: can't remove lock file."
    fi
    exit 0
}

trap on_sigterm SIGTERM SIGINT
trap on_exit EXIT

read_password() {
    printf "Password: "
    read -s password
    printf "\n"
    if [[ $(echo $password | sha256sum) != $(cat $PASSWD) ]]; then
        echo "Incorrect password."
        exit 1
    fi
}

# Lock check
if [[ -f $LOCK ]]; then
    echo >&2 'This script is already running.'
    _remove_lock=false
    read
    exit 1
fi

# Sanity tests
if [[ ! -d $DEST ]]; then
    echo >&2 'Destination directory does not exist.'
    exit 1
elif [[ ! -f $PASSWD ]]; then
    echo >&2 'Cannot find archive password.'
    exit 1
fi

varch() {
    LOCK=~/Documents/Relic/.$1
    cd $DEST
    touch $LOCK

    if [[ -d $1 ]]; then
        echo "[Compressing]"
        read_password
        printf "Hashing images...\n"
        $HASH_SCRIPT "$DEST/$1"
        printf "Backing up old archive...\n"
        [ -f $1.7z ] && mv -u $1.7z $1.7z~
        printf "Creating new archive...\n"
        7z a -p"$password" -t7z -m0=lzma -mx=8 -ms=on -mhe=on $1.7z $1
        $TEST_ARCHIVE && 7z t -p"$password" $1.7z
        printf "Removing old files...\n"
        rm -r $1/
        if $CLEAR_RECENT; then
            printf "Clearing recent documents...\n"
            :> ~/.local/share/recently-used.xbel
            printf "Clearing thumbnails...\n"
            rm -f ~/.cache/thumbnails/normal/*
            rm -f ~/.cache/thumbnails/large/*
        fi
    else
        echo "[Extracting]"
        read_password
        7z x -p"$password" $1.7z
    fi
}

if [[ $# -eq 0 ]]; then
    read -p "Which archive would you like to access? " name
    varch "$name"
elif [[ $# -gt 0 ]]; then
    varch "$1"
fi

