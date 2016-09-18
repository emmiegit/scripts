#!/bin/sh
set -e

source '/usr/local/scripts/local/encmount.sh'

rclone_sync() {
	if [ "$1" == "*.crypt" ]; then
		name="${1:0:-6}"
		src="/media/archive/Backup/$1"
		dest="Amazon Backup:/Live/$name/$uid"
	else
		name="$1"
		src="/media/archive/Backup/$1"
		dest="Amazon Backup:/Live/$1/$uid"
	fi

	echo "Synchronizing $name..."
	rclone mkdir "$dest"
	rclone sync "$src" "$dest"
}

uid="$(date +%j%Y)"

printf 'Mounting encrypted filesystems...\n'
#encmount /media/archive/Backup/Nexus\ One
#encmount /media/archive/Backup/Nexus\ Five
#encmount /media/archive/Backup/Novus\ USB

printf '\nStarting backup...\n'
rclone_sync 'Titus'
rclone_sync 'Archive Disk'
#rclone_sync 'Nexus One.crypt'
#rclone_sync 'Nexus Five.crypt'
#rclone_sync 'Novus USB.crypt'

