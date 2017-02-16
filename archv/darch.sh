#!/bin/sh
set -eu

cd "$HOME/Git/darch"
exec python3 -m darch "$@"
