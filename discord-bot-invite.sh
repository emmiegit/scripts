#!/bin/bash
set -eu

[[ $# -eq 0 ]] && exit 1
printf 'https://discordapp.com/oauth2/authorize?scope=bot%%20applications.commands&client_id=%s&permissions=%d\n' "$1" "${2:-0}"
