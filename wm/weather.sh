#!/bin/bash

location=10021

curl -s http://rss.accuweather.com/rss/liveweather_rss.asp\?locCode\=${location}               \
	| perl -ne 'if (/Currently/) {chomp;/\<title\>Currently: (.*)?\<\/title\>/; print "$1"; }' \
	| sed 's/F/°F/g'
echo
