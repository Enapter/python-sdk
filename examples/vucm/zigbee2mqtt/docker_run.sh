#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(realpath "$(dirname "$0")")"
IMAGE_TAG="${IMAGE_TAG:-"enapter-vucm-examples/$(basename "$SCRIPT_DIR"):latest"}"

bash $SCRIPT_DIR/docker_build.sh

docker run --rm -it \
	--network host \
	-e ENAPTER_LOG_LEVEL="${ENAPTER_LOG_LEVEL:-info}" \
	-e ENAPTER_VUCM_BLOB="$ENAPTER_VUCM_BLOB" \
	-e ZIGBEE_MQTT_HOST="$ZIGBEE_MQTT_HOST" \
	-e ZIGBEE_MQTT_PORT="$ZIGBEE_MQTT_PORT" \
	-e ZIGBEE_MQTT_USER="$ZIGBEE_MQTT_USER" \
	-e ZIGBEE_MQTT_PASSWORD="$ZIGBEE_MQTT_PASSWORD" \
	-e ZIGBEE_MQTT_TOPIC="$ZIGBEE_MQTT_TOPIC" \
	-e ZIGBEE_SENSOR_MANUFACTURER="$ZIGBEE_SENSOR_MANUFACTURER" \
	-e ZIGBEE_SENSOR_MODEL="$ZIGBEE_SENSOR_MODEL" \
	"$IMAGE_TAG"
