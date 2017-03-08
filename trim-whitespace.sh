#!/bin/bash

trim_whitespace() {
	printf '%s' "$1" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}

