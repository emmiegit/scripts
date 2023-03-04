#!/bin/bash

# Wrapper for trash-cli commands.
# When invoked with no arguments, lists current trash items. Otherwise trashes the specified files.

if [[ $# -eq 0 ]]; then
	exec trash-list
else
	exec trash-put "$@"
fi
