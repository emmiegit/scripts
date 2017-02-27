#!/bin/sh
set -u
exec maim -s "$HOME/Incoming/$(date +%s).png"

