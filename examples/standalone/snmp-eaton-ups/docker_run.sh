#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(realpath "$(dirname "$0")")"
IMAGE_TAG="${IMAGE_TAG:-"enapter-standalone-examples/$(basename "$SCRIPT_DIR"):latest"}"

bash $SCRIPT_DIR/docker_build.sh

docker run --rm -it \
	--network host \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	-e ENAPTER_SNMP_HOST="$ENAPTER_SNMP_HOST" \
	-e ENAPTER_SNMP_PORT="$ENAPTER_SNMP_PORT" \
	-e ENAPTER_SNMP_COMMUNITY="$ENAPTER_SNMP_COMMUNITY" \
	"$IMAGE_TAG"
