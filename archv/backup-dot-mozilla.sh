#!/bin/bash
set -euo pipefail

archive_location='/media/archive/backup'
archive_name='dotmozilla.tar.xz'
archive="$archive_location/$archive_name"
tabs="$archive_location/$tabs_name"
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
/usr/local/scripts/archv/backup-firefox-tabs.sh "$tabs"
