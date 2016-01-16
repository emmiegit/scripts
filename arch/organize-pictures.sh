#!/bin/bash
set -e

CONFIRM_DELETE=false
RECURSIVE=false
OPEN='feh -g 840x600'
LIST_DIRS=false
LIST_CMD='/bin/ls -d --color=tty */ .*/'

confirmation() {
    if $CONFIRM_DELETE; then
        read -p "Are you sure you would like to delete this file? [y/N] " response
        case $response in
            yes) return 0 ;;
            y) return 0 ;;
            Y) return 0 ;;
            *) return 1 ;;
        esac
    else
        return 0
    fi
}

movefile() {
    while true; do
        if $LIST_DIRS; then
            $LIST_CMD
        fi

        read -p "To which directory would you like to move $1 to? " dest
        if [[ -z $dest ]] || [ "$dest" == "." ]; then
            return
        elif [ "$dest" == "!" ]; then
            confirmation && trash "$1" && return
        elif [[ -d $dest ]]; then
            mv "$1" "$dest"
            return
        else
            echo "That's not a valid directory."
        fi
    done
}

organize() {
    prev=`pwd`
    cd "$1"
    for fn in *; do
        if [[ -d $fn ]] && $RECURSIVE; then
            echo "Recursively organizing $fn..."
            organize "$fn"
        elif file "$fn" | grep -q "image"; then
            $OPEN "$fn" &
            movefile "$fn"
            kill $! ||:
        else
            echo "Skipping $fn..."
        fi
    done

    cd "$prev"
}

if [[ $# -eq 0 ]]; then
    echo "Usage: $(dirname $0) directory-to-organize..."
    exit 1
fi

while [[ $# -gt 0 ]]; do
    organize "$1"
    shift
done

