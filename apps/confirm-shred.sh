#!/usr/bin/env bash

if zenity --question \
		  --title "Permanently delete files." \
		  --text "Are you sure you want to shred these files?\nThey will be permanently deleted from your computer."; then
	shred -u "$@"
fi

