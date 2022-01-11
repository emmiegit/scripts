#!/bin/bash
set -eu

totp_code="$(
	pass show misc/totp-codes |
	jq -r -c '.[] | select( .name == "Point: Amazon Web Services" ) | .secret' |
	oathtool --base32 --totp -
)"

echo "Logging in... (TOTP code $totp_code)"
"$HOME/git/point-tools/scripts/aws-get-session-token.sh" point "$totp_code"
