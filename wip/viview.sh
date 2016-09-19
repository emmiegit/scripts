#!/bin/bash

# Accept piped input from a file and use vim's "view" on the data.
#
# Copyright (C) 2015 Ammon Smith
# Licensed under the MIT License.

exit 0 # fixme
TEMP_FILE=$(mktemp /tmp/viview-XXXXXX.txt)

while read LINE; do
    echo "$LINE" >> "$TEMP_FILE"
done < "${1:-/dev/stdin}"

view "$TEMP_FILE"

