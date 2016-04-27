#!/usr/bin/env bash
set -euv

interactive_replace() {
    grep -e "$1" /etc/mime.types | \
    while read -r mime_type; do
        read -rp "$mime_type: " desktop_file

        if [[ -n $desktop_file ]]; then
            if [[ "$desktop_file" != "*.desktop" ]]; then
                desktop_file="${desktop_file}.desktop"
            fi

            xdg-mime default "$desktop_file" "$mime_type"
        fi
    done
}

if [[ $# -eq 0 ]]; then
    printf >&2 'Usage: %s [regular-expression]...\n' "$(basename "$0")"
    exit 1
fi

for regex in "$@"; do
    interactive_replace "$regex"
done

