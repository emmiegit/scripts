#!/bin/bash
set -eu

until pgrep Xorg; do
    sleep 10
done

sleep 30
nvidia-settings --load-config-only

# vim: set ft=sh:
