#!/bin/sh
set -e

encmount() {
    if ! mount | grep -q "$1"; then
        echo "Mounting $1..."
        encfs "$1.crypt" "$1"
    else
        echo "$1 already mounted."
    fi
}

for dir in "$@"; do
    encmount "/media/archive/Backup/$dir"
done

