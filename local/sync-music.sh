#!/bin/bash
set -eu

cd "${0%/*}"
./sync-titus.sh /home/emmie/music ~/music --exclude .git
