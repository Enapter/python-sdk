#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/ats3-backup:latest"
SCRIPT_DIR="$(realpath "$(dirname "$0")")"

docker build --file backup.Dockerfile --tag "$IMAGE_TAG" "$SCRIPT_DIR"
