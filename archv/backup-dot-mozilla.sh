#!/bin/bash
set -euo pipefail

archive_location='/media/archive/backup'
archive_name='dotmozilla.tar.xz'
archive="$archive_location/$archive_name"
gpg_key='2C3CF0C7'
tar_program='/usr/bin/tar'

clean() {
	rm -f "$archive"
}

trap clean EXIT SIGINT SIGTERM

"$tar_program" -cJf "$archive" ~/.mozilla
gpg --yes -er "$gpg_key" "$archive"
