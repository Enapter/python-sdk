#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

IMAGE_TAG="tyenap/ats3:latest"

docker build --file ats3.Dockerfile --tag "$IMAGE_TAG"

