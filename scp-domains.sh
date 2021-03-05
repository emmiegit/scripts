#!/bin/bash
set -eu

domains=(
	'scp-wiki.wikidot.com'
	'scpwiki.com'
	'scp-wiki.net'
)

function check_site() {
	echo "URL BEING CHECKED: $1"
	curl -iI "$1" || true
	echo "----------------------------------------------------"
}

for domain in "${domains[@]}"; do
	check_site "http://$domain/"
	check_site "https://$domain/"
done
