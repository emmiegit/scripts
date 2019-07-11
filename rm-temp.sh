#!/bin/bash
rm -fv \
	"$HOME/incoming"/random-*.pdf \
	/tmp/error.dump.* \
	/tmp/racerd_* \
	/tmp/sbt*.log \
	/tmp/service-authors.* \
	/tmp/ti-*.log \
	/tmp/tsserver_*.log \
	/tmp/tmp* \
	/tmp/ycm*.log

rm -rfv \
	"/tmp/$USER/aur"/* \
	/tmp/e-c-ts-* \
	/tmp/loandocs* \
	/tmp/openapi.* \
	/tmp/sitespeed.*
