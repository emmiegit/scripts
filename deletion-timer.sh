#!/bin/bash
set -eu

if [[ $# -eq 0 ]]; then
	echo "Usage: $0 current-vote"
	exit 1
fi

if [[ $1 -gt -10 ]]; then
	echo "Vote must be -10 or lower"
	exit 1
fi

cat << EOF
Staff Post - Deletion Vote

---

TODO: something is messed up with the time zone

Beginning deletion vote at $1.

[[iframe http://home.helenbot.com/tools/timer.html?time=$(date +%s)000&type=del style="width: 500px; height: 250px; border: 0;"]]

**If you are not the author and you want to rewrite this article, you may reply to this post asking for the opportunity to do so. Please obtain permission from the author (or the Rewrite Team if this article is older than 6 months) and make sure you copy the page source to your sandbox. Please do __not__ reply to this post for any other reason unless you are staff.**
EOF
