#!/bin/bash
rm -fv \
	/tmp/*.cdtor.[co] \
	/tmp/error.dump.* \
	/tmp/racerd_* \
	/tmp/rust_language_server_* \
	/tmp/sbt*.log \
	/tmp/service-authors.* \
	/tmp/ti-*.log \
	/tmp/tsserver_*.log \
	/tmp/ycm*.log

rm -rfv \
	"/tmp/$USER/aur"/* \
	/tmp/brz-diff* \
	/tmp/e-c-ts-* \
	/tmp/loandocs* \
	/tmp/openapi.* \
	/tmp/rustc* \
	/tmp/sitespeed.* \
	/tmp/tmp* \
	/tmp/ts-node-*
