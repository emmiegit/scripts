#!/bin/bash
/usr/share/playonlinux/playonlinux --run "League of Legends" %F &
echo "$$" | "$(dirname "$0")/league-loop"

