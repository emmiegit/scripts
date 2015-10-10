#!/usr/bin/env bash

DEST=$1
[ -z "$2" ]  && PASSWD=.passwd || PASSWD=$2
[ -z "$3" ] && HASH_SCRIPT=hash_media.py || HASH_SCRIPT=$3

if [[ -f .$1 ]]; then
    echo "This script is already running."
    read
    exit 1
fi

cd $DEST
touch .$1

if [ -d $DEST/$1/ ]; then
    echo "[Compressing]"
    printf "Password: " &&
    read -s password &&
    printf "\n" &&
    if [[ $(echo $password | sha1sum) != $(cat $PASSWD) ]]; then
        rm $DEST/.$1
        printf "Incorrect password. "
        exit 1
    fi
    printf "Hashing images...\n" &&
    $HASH_SCRIPT $1/
    printf "Backing up old archive...\n"
    [ -f $1.rar ] && mv -u $1.rar $1.rar~
    printf "Compressing files...\n" && {
        rar a -hp$password -t $1.rar $1/*
    } &&
    printf "Removing old files...\n" &&
    rm -rf $1/
else
    echo "[Extracting]"
    rar x $1.rar
fi

rm .$1
echo "Finished."

