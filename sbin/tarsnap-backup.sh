#!/bin/bash
set -eu

archive="$(date +%B-%d-%Y | tr '[:upper:]' '[:lower:]')"
locations=()

for argument in "$@"; do
	case "$argument" in
		root)
			locations+=(
				"$HOME"
				"/etc"
				"/var"
			)
			;;
		archive)
			locations+=('/media/archive/git')
			;;
		media)
			locations+=('/media/media')
			;;
		*)
			echo "Unknown location specifier: $1"
			exit 1
	esac
done

exec \
	ionice -c 3 \
	nice -n 10 \
		tarsnap -c \
		-f "$archive-$1" \
		-v \
		--print-stats \
		"${locations[@]}" \
		> /var/log/tarsnap.log \
		2>&1

# Cron backup:
# 0 20 1 * * /usr/local/scripts/sbin/tarsnap-backup.sh root
# 0 21 1 * * /usr/local/scripts/sbin/tarsnap-backup.sh archive
# 0 22 1 */2 * /usr/local/scripts/sbin/tarsnap-backup.sh media
