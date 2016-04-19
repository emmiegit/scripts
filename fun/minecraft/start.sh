#!/usr/bin/env bash 
set -eu

BACKUP_PID=

finish() {
    rm -f lock
}

backup() {
    sleep 30
    while true; do
        sleep 3000
        dest="backups/$(date +%s)"
        printf 'Making backup world at "%s"...' "$(basename "$dest")"
        mkdir -p "$dest"
        cp -at "$dest" world/*
        echo 'done.'
    done
}

main() {
    if [[ -f lock ]]; then
        printf >&2 'Server is already running.\n'
        exit 1
    else
        touch lock
    fi

    if [[ -f make_backups ]]; then
        backup &
        BACKUP_PID=$!
    fi

    java -Xms2G -Xmx12G -jar minecraft_server.jar nogui
    [[ -f make_backups ]] && kill $BACKUP_PID
}

trap finish SIGINT SIGTERM EXIT
main

