#!/bin/bash
set -e

FILE='/usr/local/scripts/dat/hamlet.txt'
COPY="$(mktemp /tmp/hamlet-XXXXXXXXX.txt)"

if [[ ! -z $1 ]]; then
	EDITOR=$1
elif [[ ! -z $VISUAL ]]; then
	EDITOR=$VISUAL
elif [[ ! -z $EDITOR ]]; then
	: # $EDITOR is already $EDITOR, so do nothing
else
	EDITOR=vi
fi

cp -f "$FILE" "$COPY"
chmod +w "$COPY"
"$EDITOR" "$COPY" 2> /dev/null
rm -f "$COPY"
