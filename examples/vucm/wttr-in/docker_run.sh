#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(realpath "$(dirname "$0")")"
IMAGE_TAG="${IMAGE_TAG:-"enapter-vucm-examples/$(basename "$SCRIPT_DIR"):latest"}"

docker build --tag "$IMAGE_TAG" "$SCRIPT_DIR"

docker run --rm -it \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	-e WTTR_IN_LOCATION="$WTTR_IN_LOCATION" \
	"$IMAGE_TAG"
