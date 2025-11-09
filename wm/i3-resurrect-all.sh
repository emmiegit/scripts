#!/bin/bash
set -eu

for workspace in {1..4}; do
	i3-resurrect restore --workspace "$workspace"
done
