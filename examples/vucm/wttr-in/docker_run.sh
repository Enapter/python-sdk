#!/bin/bash

docker run --rm -it \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	-e WTTR_IN_LOCATION="$WTTR_IN_LOCATION" \
	"$(docker build --quiet "$(dirname "$0")")"
