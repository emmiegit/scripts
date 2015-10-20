#!/usr/bin/env bash
set -e

LOCK=~/.$1
DEST=~/
HASH_SCRIPT=~/Scripts/hash_media.py
PASSWD=~/Scripts/.passwd
CLEAR_RECENT=true

on_sigterm() {
    echo "Caught user interrupt, closing down."
    if [[ -f $LOCK ]]; then
        rm -f $LOCK
    else
        echo "Warning: can't find lock file."
    fi
    read
    exit 1
}

on_exit() {
    echo "Finished."
    if [[ -f $LOCK ]]; then
        rm -f $LOCK
    else
        echo "Warning: can't find lock file."
    fi
    read
    exit 1
    [[ -f $LOCK ]] && rm $LOCK
    echo "Finished."
    exit 0
}

trap on_sigterm SIGTERM
trap on_exit EXIT

read_password() {
    printf "Password: "
    read -s password
    printf "\n"
    if [[ $(echo $password | sha1sum) != $(cat $PASSWD) ]]; then
        rm $LOCK
        echo "Incorrect password."
        exit 1
    fi
}

if [[ -f $LOCK ]]; then
    echo "This script is already running."
    read
    exit 1
fi

cd $DEST
touch $LOCK

if [[ -d $DEST/$1/ ]]; then
    echo "[Compressing]"
    read_password
    printf "Hashing images...\n"
    $HASH_SCRIPT $1/
    printf "Backing up old archive...\n"
    [ -f $1.7z ] && mv -u $1.7z $1.7z~
    7z a -p"$password" -t7z -m0=lzma -mx=8 -ms=on -mhe=on $1.7z $1
    7z t -p"$password" $1.7z
    printf "Removing old files...\n"
    rm -r $1/
    if $CLEAR_RECENT && [ -d ~/.local/share ]; then
        printf "Clearing recent documents...\n"
        :> ~/.local/share/recently-used.xbel
    fi
else
    echo "[Extracting]"
    read_password
    7z x -p"$password" $1.7z
fi
