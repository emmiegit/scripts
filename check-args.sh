#!/bin/bash

argno=1

printf '$#: %d\n' "$#"
printf '0: <%s>\n' "$0"

for arg in "$@"; do
	printf '%d: <%s>\n' "$argno" "$arg"
	((argno++))
done

