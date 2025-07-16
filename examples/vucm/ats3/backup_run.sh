#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/ats3-backup:latest"

docker run --rm -it \
	--name "ats3" \
	--network host \
	--mount type=volume,dst=/app \
	--env-file env.list \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	"$IMAGE_TAG"
