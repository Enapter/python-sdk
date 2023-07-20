#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(realpath "$(dirname "$0")")"
IMAGE_TAG="${IMAGE_TAG:-"enapter-vucm-examples/$(basename "$SCRIPT_DIR"):latest"}"

docker build --progress=plain --tag "$IMAGE_TAG" "$SCRIPT_DIR"
