#!/usr/bin/env bash 

finish() {
    rm -f lock
    [[ ! -z $BAK_PID ]] && kill $BAK_PID
}

backup() {
    sleep 30
    while true; do
        sleep 3000
        dest=world.bak/$(date +%s)
        printf 'Making backup world at "%s"...' "$(basename $dest)"
        mkdir -p $dest
        cp -at $dest world/*
        echo 'done.'
    done
}

main() {
    if [ -f lock ]; then
        read -p 'Server is already running.'
        exit 1
    else
        touch lock
    fi

    [ -f make_backups ] && $(cat make_backups) && backup &
    BAK_PID=$!
    exec java -jar -Xms2G -Xmx12G -jar minecraft_server.jar nogui
}

trap finish SIGINT SIGTERM EXIT
main

