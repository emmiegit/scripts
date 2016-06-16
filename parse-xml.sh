#!/usr/bin/env bash

read_tag() {
	local IFS='>'
	read -rd '<' ENTITY CONTENT
}

if [[ $# -gt 0 ]]; then
	while read_tag; do
		for arg in "$@"; do
			if [[ "$ENTITY" == "$arg" ]]; then
				printf '%s:%s\n' "$ENTITY" "$CONTENT"
			fi
		done
	done
else
	while read_tag; do
		if [[ ${ENTITY:0:1} != '/' ]]; then
			printf '%s:%s\n' "$ENTITY" "$CONTENT"
		fi
	done
fi

