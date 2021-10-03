#!/bin/bash
set -eu

# Based on https://stackoverflow.com/a/40966234

sudo docker image build -t build-context -f - . <<EOF

FROM busybox
COPY . /build-context
CMD find /build-context
EOF
