#!/bin/bash
set -eux

env \
	ADMIN_BASE_URL=http://localhost:3000 \
	BORROWER_BASE_URL=http://localhost:3000 \
	python3 \
		-m pytest \
		--base-url http://localhost:3000 \
		-s -rwx \
		--driver Chrome \
		--capability resolution 1440x1440 \
		"$@"
