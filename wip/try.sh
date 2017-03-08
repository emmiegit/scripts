#!/bin/bash

try() {
	local DETACH=false
	local DISOWN=false

	while true; do
	    case "$1" in
	        --detach) DETACH=true ;;
	        --disown) DISOWN=true ;;
	        *) break ;;
	    esac
	    shift
	done

	printf "$1"
	shift

	if $DISOWN; then
	    $@ >/dev/null 2>&1 & disown 
	elif $DETACH; then
	    $@ >/dev/null 2>&1 &
	else
	    $@ >/dev/null 2>&1
	fi

	if [[ $? -eq 0 ]]; then
	    printf " [\e[32m\e[1mok\e[0m]\n"
	else
	    printf " [\e[31m\e[1merror\e[0m]\n"
	fi
}

