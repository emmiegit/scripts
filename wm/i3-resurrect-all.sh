#!/bin/bash
set -eu

for workspace in {1..4}; do
	i3-resurrect restore --directory "$HOME/.config/i3/i3-resurrect" --workspace "$workspace"
done
