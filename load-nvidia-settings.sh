#!/bin/bash
set -eu

until pgrep Xorg; do
    sleep 20
done

nvidia-settings --load-config-only

# vim: set ft=sh:
