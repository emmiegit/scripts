#!/bin/sh

# League via Wine sometimes leaves random processes behind, spinning at 100%
# and wasting CPU cycles. This script kills them.

pkill -u "$USER" League
pkill -u "$USER" LoL

