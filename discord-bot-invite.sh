#!/bin/bash
set -eu

[[ $# -eq 0 ]] && exit 1
printf 'https://discordapp.com/oauth2/authorize?&client_id=%s&scope=bot&permissions=0\n' "$1"

