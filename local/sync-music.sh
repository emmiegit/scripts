#!/bin/bash
set -eu

cd "${0%/*}"
./sync-titus.sh /media/media/music ~/music --exclude .git
