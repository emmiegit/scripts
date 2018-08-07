#!/bin/sh
cd "$HOME/documents/relic/git/osu"
exec git describe --always --tags
