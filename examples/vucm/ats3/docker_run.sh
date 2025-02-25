#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/standalone-devices:latest"

docker run --rm -it \
	--name "ni-daq" \
	--network host \
	--env-file env.list \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	"$IMAGE_TAG"
