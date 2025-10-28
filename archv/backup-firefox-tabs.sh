#!/bin/bash
set -euo pipefail

firefox_profile='0s56fc3h.dev-edition-default'
temp_file="$(mktemp /tmp/sessionstore-XXXXXX.json)"
output="$1"

dejsonlz4 "$HOME/.mozilla/firefox/$firefox_profile/sessionstore-backups/recovery.jsonlz4" "$temp_file"
jq -r '[.windows[].tabs[].entries[]] | reverse | unique_by(.docshellUUID)[].url' "$temp_file" > "$output"
