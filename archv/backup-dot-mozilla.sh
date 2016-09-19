#!/bin/bash
set -eu

ARCHIVE_LOCATION='/media/archive/Backup'
ARCHIVE_NAME='dotmozilla.tar.xz'
ARCHIVE="$ARCHIVE_LOCATION/$ARCHIVE_NAME"
GPG_KEY='2C3CF0C7'

tar -cJf "$ARCHIVE" ~/.mozilla
gpg --yes -er "$GPG_KEY" "$ARCHIVE"
rm "$ARCHIVE"

