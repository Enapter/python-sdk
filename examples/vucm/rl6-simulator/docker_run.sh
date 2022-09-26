#!/bin/bash

docker run --rm -it \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	-e ENAPTER_VUCM_CHANNEL_ID="rl6" \
	"$(docker build --quiet "$(dirname "$0")")"
