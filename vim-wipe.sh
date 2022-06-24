#!/bin/bash
set -eu

# Cleans up vim backup files, which can accumulate if you go a long time without wiping them.

rm -f "/tmp/$USER/vim_undo/"* "$HOME/.vim_runtime/backups/"*
