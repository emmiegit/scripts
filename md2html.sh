#!/usr/bin/env bash
set -eu

DID_SOMETHING=false

recursively_convert() {
    local changed=false

    for file in *; do
        "$changed" && printf '[DIR] %s\n' "$(basename "$(pwd)")"

        if [[ -d $file ]]; then
            cd "$file"
            recursively_convert
            cd ..
        elif [[ $file == *.md ]]; then
            local target="${file:0:-3}.html"

            if [[ ! -f $target ]] || [[ $file -nt $target ]]; then
                changed=true
                DID_SOMETHING=true
                printf '[MD] %s\n' "$file"
                markdown "$file" > "$target"
            fi
        fi
    done
}

[[ $# -gt 0 ]] && cd "$1"
recursively_convert
"$DID_SOMETHING" || printf 'Nothing to do.\n'

