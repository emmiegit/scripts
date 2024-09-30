#!/bin/bash
set -eu

source "${0%/*}/borg-source.sh"

exec \
	ionice -c 3 \
	nice -n 10 \
		borg delete -v "$backup" "$@"
