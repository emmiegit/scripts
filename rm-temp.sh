#!/bin/bash
rm -fv \
	"$HOME/incoming"/random-*.pdf \
	/tmp/error.dump.* \
	/tmp/racerd_* \
	/tmp/service-authors.* \
	/tmp/ti-*.log \
	/tmp/tsserver_*.log \
	/tmp/tmp* \
	/tmp/ycm*.log

rm -rfv \
	/tmp/e-c-ts-* \
	/tmp/openapi.* \
	/tmp/sitespeed.*
