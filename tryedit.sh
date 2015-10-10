#!/usr/bin/env bash

[ -z "$1" ] && FILE=.hamlet || FILE=$1
[ -z "$EDITOR" ] && EDITOR=vi

cd ~/Scripts/
cp $FILE $FILE.txt
chmod +w $FILE.txt
$EDITOR $FILE.txt
rm $FILE.txt

