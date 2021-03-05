#!/bin/bash
set -eu

domains=(
	'scpwiki.com'
	'www.scpwiki.com'
	'scp-wiki.net'
	'www.scp-wiki.net'
	'scp-wiki.wikidot.com'
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
