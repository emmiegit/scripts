#!/bin/bash

FILE='/usr/local/scripts/dat/hamlet.txt'

if [[ ! -z $1 ]]; then
    EDITOR=$1
elif [[ ! -z $VISUAL ]]; then
    EDITOR=$VISUAL
elif [[ ! -z $EDITOR ]]; then
    : # $EDITOR is already $EDITOR, so do nothing
else
    EDITOR=vi
fi

cp -f "${FILE}" ".${FILE}"
chmod +w ".${FILE}"
"$EDITOR" ".${FILE}" 2> /dev/null
rm ".${FILE}"

