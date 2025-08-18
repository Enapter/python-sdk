#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/ats3-backup:latest"

docker build --file backup.Dockerfile --tag "$IMAGE_TAG"

docker push tyenap/ats3-backup:latest
