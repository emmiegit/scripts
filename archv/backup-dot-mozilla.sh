#!/bin/bash
set -euo pipefail

archive_location='/media/archive/backup'
archive_name='dotmozilla.tar.xz'
archive="$archive_location/$archive_name"
tabs_name='firefox_tabs.txt'
tabs="$archive_location/$tabs_name"
firefox_profile='0s56fc3h.dev-edition-default'
gpg_key='2C3CF0C7'
tar_program='/usr/bin/tar'
temp_dir="$(mktemp -d /tmp/dot-mozilla-XXXXXXXXX)"

clean() {
	rm -f "$archive"
	rm -rf "$temp_dir"
}

trap clean EXIT SIGINT SIGTERM

# Copy all files first so we avoid modified-while-read errors.
cp -a ~/.mozilla "$temp_dir"

# Create compressed archive
(
	cd "$temp_dir"
	"$tar_program" -cJf "$archive" .mozilla
)

# Encrypt using the given GPG key
gpg --yes -er "$gpg_key" "$archive"

# Export open browser tabs
dejsonlz4 "$HOME/.mozilla/firefox/$firefox_profile/sessionstore.jsonlz4" "$temp_dir/sessionstore.json"
jq -r '.windows[].tabs[].entries[].url' "$temp_dir/sessionstore.json" > "$tabs"
