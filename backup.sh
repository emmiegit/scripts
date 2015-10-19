#!/usr/bin/env bash
set -e

salt=39sjKa0
gpgkey=2C3CF0C7
uid=`date +%s`
duply_profile=standard
lock=/tmp/$USER-duply.lock
logfile=/tmp/$USER-duply-$uid.log
filelist=$HOME/Temporary/backup-filelist.txt

[ -f $lock ] && echo "A backup is already running!" && exit 1
touch $lock

notify() {
    notify-send "$1" "$2" -i /usr/share/pixmaps/deja-dup.png
}

on_exit() {
    rm -f $lock
    remove_password
    exit $?
}

on_sigterm() {
    rm -f $lock
    remove_password
    notify "Backup was cancelled." "Check logfile at $logfile."
    exit $?
}

trap on_exit EXIT
trap on_sigterm SIGTERM

run() {
    ionice -c3 duply $duply_profile $@
}

gen_password() {
    echo $salt-$GPG_PW | sha256sum > .bakpasswd
}

add_password() {
    if [ ! -f $(dirname $0)/.bakpasswd ]; then
        echo "Cannot find backup password file. Aborting."
        exit 1
    fi

    GPG_PW=$(zenity --password --title "Enter GPG key passphrase to start backup")

    if [[ `echo $salt-$GPG_PW | sha256sum` != `cat $(dirname $0)/.bakpasswd` ]]; then
        echo "Password is invalid. Aborting."
        exit 1
    fi

    sed -i "s/GPG_PW=\$/GPG_PW=$GPG_PW/" ~/.duply/$duply_profile/conf
}

remove_password() {
    source ~/.duply/$duply_profile/conf
    sed -i "s/GPG_PW=$GPG_PW/GPG_PW=/" ~/.duply/$duply_profile/conf
}

main() {
    notify "Backup started" "Running in background. Check logfile at $logfile."
    run backup >> $logfile
    run list > $filelist
    gpg -er $gpgkey $filelist
    shred -u $filelist
    notify "Backup finished." "Check logfile at $logfile."
}

add_password
[[ $# -eq 0 ]] && main || duply $duply_profile $@
