#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/ats3:latest"
SCRIPT_DIR="$(realpath "$(dirname "$0")")"

docker build --file ats3.Dockerfile --tag "$IMAGE_TAG" "$SCRIPT_DIR"
