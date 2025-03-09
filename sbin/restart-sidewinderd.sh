#!/bin/sh

# This script is used when the computer is being suspended.
# Do not remove without updating its caller.

sleep 1
systemctl restart sidewinderd
