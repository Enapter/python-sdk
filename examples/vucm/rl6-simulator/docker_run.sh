#!/bin/bash

docker run --rm -it \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	"$(docker build --quiet "$(dirname "$0")")"
