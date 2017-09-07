#!/bin/bash
set -eu

archive_location='/media/archive/Backup'
archive_name='dotmozilla.tar.xz'
archive="$archive_location/$archive_name"
gpg_key='2C3CF0C7'

clean() {
	rm -f "$archive"
}

tar -cJf "$archive" ~/.mozilla
trap clean EXIT
gpg --yes -er "$gpg_key" "$archive"

