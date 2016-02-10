#!/bin/sh

# League via Wine sometimes leaves random processes behind, spinning at 100%
# and wasting CPU cycles. This script kills them.

pkill -fu "$USER" League
pkill -fu "$USER" LoLLauncher

