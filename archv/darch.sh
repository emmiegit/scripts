#!/bin/sh
set -eu

cd "$HOME/git/darch"
exec python3 -m darch -d "$HOME/documents/relic/private" "$@"
