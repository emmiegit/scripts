#!/bin/bash
set -euo pipefail

archive_location='/media/archive/Backup'
archive_name='dotmozilla.tar.xz'
archive="$archive_location/$archive_name"
gpg_key='2C3CF0C7'
tar_program='/usr/bin/tar'

clean() {
	rm -f "$archive"
}

"$tar_program" -cJf "$archive" ~/.mozilla
trap clean EXIT
gpg --yes -er "$gpg_key" "$archive"

