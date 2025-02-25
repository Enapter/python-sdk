#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/ats3:latest"

docker run --rm -it \
	--name "ni-daq" \
	--network host \
	--env-file env.txt \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	"$IMAGE_TAG"
