#!/bin/bash
set -eu

# Wipes Nomacs' image history, which it stories
# in the *configuration file* for some annoying reason.
#
# So much for consistent / steady state configuration files.

if [[ $# -eq 0 ]]; then
	filename="$HOME/.config/nomacs/Image Lounge.conf"
else
	filename="$1"
fi

sed -i -E -e 's/^(lastDir|recentFiles|recentFolders)=.+/\1=/' "$filename"
