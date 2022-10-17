#!/bin/bash

docker run --rm -it \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	-e MIIO_IP="$MIIO_IP" \
	-e MIIO_TOKEN="$MIIO_TOKEN" \
	"$(docker build --quiet "$(dirname "$0")")"
