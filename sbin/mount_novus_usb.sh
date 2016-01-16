#!/bin/sh
set -e

if [ $# -eq 0 ]; then
    echo >&2 'You must pass the device as an argument.'
    echo >&2 'Generally it is located at /dev/sdc1, but you'
    echo >&2 'should check lsblk first to be sure.'
    exit 1
fi

sudo mkdir -p /media/ammon/Novus
sudo mount -o gid=1000,uid=1000 $1 /media/ammon/Novus

