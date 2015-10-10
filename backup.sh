#!/usr/bin/env bash
set -e

# Be sure to replace the "." with the actual full path of the directory when you move it to your computer.
IFS=$'\n'
SAVE_DIRECTORIES=($(cat ./backup-directories))
BACKUP_LOCATION="file:///mnt/Backup-Disk/My Stuff"
GPG_KEY=2C3CF0C7 # The key id
PROMPT_BEFORE_EXIT=false

echo() {
    builtin echo $@ | tee -a ./backup.log
}

on_sigterm() {
    echo "Caught user interrupt."
    $PROMPT_BEFORE_EXIT && read
    exit 1
}

on_exit() {
    if [[ $? -eq 0 ]]; then
        echo "Done."
        $PROMPT_BEFORE_EXIT && read
        exit 0
    else
        echo -e "\e[31mErrors have occurred while backing up.\e[0m"
        $PROMPT_BEFORE_EXIT && read
        exit 1
    fi
}

trap "on_sigterm" SIGTERM
trap "on_exit" EXIT

pexec() {
    echo $@
    $@
}

backup() {
    for dir in ${SAVE_DIRECTORIES[@]}; do
        pexec duplicity --full-if-older-than 1M --encrypt-key $GPG_KEY --allow-source-mismatch "$dir" "$BACKUP_LOCATION"
    done
}

remove_old() {
    pexec duplicity remove-older-than 1Y "$BACKUP_LOCATION"
}

cleanup() {
    pexec duplicity cleanup "$BACKUP_LOCATION"
}

print_help() {
    echo "Usage: $(basename $0) [clean | help]"
    echo "Commands:"
    echo " (none) - Create an incremental backup of the directories specified in \"backup-directories\". This command will ensure that a full backup is made at least once a month in addition to the incremental backups."
    echo " clean  - Removes any unnecessary files from the backup directory via duplicity's \"cleanup\" directive."
    echo " help   - Prints this help message."
}

main() {
    backup
    remove_old
}

if [[ $# -eq 0 ]]; then
    main
elif [[ $1 == help ]]; then
    print_help
elif [[ $1 == clean ]]; then
    cleanup
else
    echo "Unknown command \"$1\". Try using \"help\"."
fi

