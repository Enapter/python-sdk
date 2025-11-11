#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(realpath "$(dirname "$0")")"
IMAGE_TAG="${IMAGE_TAG:-"enapter-standalone-examples/$(basename "$SCRIPT_DIR"):latest"}"

docker build --tag "$IMAGE_TAG" "$SCRIPT_DIR"

docker run --rm -it \
	--network host \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	-e ENAPTER_STANDALONE_COMMUNICATION_CONFIG="$ENAPTER_STANDALONE_COMMUNICATION_CONFIG" \
	"$IMAGE_TAG"
