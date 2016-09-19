#!/bin/bash

chperms() {
	cd "$1" || return 1
	for item in *; do
		if [[ -d $item ]]; then
			chperms "$item"
		elif [[ $item == *.sh ]] || [[ $item == *.py ]]; then
			echo chmod -v 775 "$item"
		fi
	done
	cd ..
}

chperms .

