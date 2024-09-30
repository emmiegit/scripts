#!/bin/bash
set -eu

source "${0%/*}/borg-source.sh"
exec borg list -v "$backup"
