#!/bin/bash

readonly repo="$HOME/git/mortgage"

exec env \
	NODE_ENV=test \
	PORT=18130 \
	mocha \
		--no-timeouts \
		--require "$repo/mortgage/backend/lib/type-check-transform.js" \
		--exit "$repo/mortgage/backend/test/lib/serializers/"
