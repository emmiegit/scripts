#!/bin/bash
set -eu

gfile="/run/user/$EUID/gmail_stopped"

if [[ -f "$gfile" ]]; then
	sig='CONT'
	echo 'Continuing...'
else
	touch "$gfile"
	sig='STOP'
	echo 'Stopping...'
fi

pkill "-$sig" -u "$USER" gmail-check-notify
pkill "-$sig" -u "$USER" claws-mail
