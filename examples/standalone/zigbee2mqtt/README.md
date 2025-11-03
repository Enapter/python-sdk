# Zigbee Sensor (MQTT)

This example describes the implementation of the Standalone Device concept
using the opensource [Enapter
python-sdk](https://github.com/Enapter/python-sdk) for monitoring Zigbee Sensor
via MQTT protocol (Zigbee2Mqtt).

In order to use this Standalone Device you need to have
[Zigbee2MQTT](https://www.zigbee2mqtt.io/guide/installation/) and some MQTT
broker (for example [Mosquitto](https://mosquitto.org)) running.

As an example in this guide we will use the following dummy settings for
configuration:

- MQTT Broker Address: 192.168.192.190
- MQTT Broker Port: 9883
- MQTT User: mqtt_user
- MQTT Password: mqtt_password
- Device MQTT topic: zigbee2mqtt/MyDevice

## Requirements

It is recommended to run this Standalone Device using Docker and Docker
Compose. This will ensure that environment is correct.

The MQTT broker must be reachable from the computer where the Docker Container
will be running.

## Step 1. Create Standalone Device in Enapter Cloud

Log in to the Enapter Cloud, navigate to the Site where you want to create
Standalone Device and click on `Add new` button in the Standalone Device
section.

After creating Standalone Device, you need to Generate and save Configuration
string also known as `ENAPTER_STANDALONE_COMMUNICATION_CONFIG` as well as save
UCM ID which will be needed for the next step.

## Step 2. Upload Blueprint into the Cloud

The general case [Enapter Blueprint](https://marketplace.enapter.com/about)
consists of two files - declaration in YAML format (manifest.yaml) and logic
written in Lua. Howerver for this case the logic is written in Python.

But for both cases we need to tell Enapter Cloud which telemetry we are going
to send and store and how to name it.

The easiest way to do that - using [Enapter
CLI](https://github.com/Enapter/enapter-cli) to upload manifest.yaml into
Cloud. The other option is to use [Web
IDE](https://developers.enapter.com/docs/tutorial/uploading-blueprint).

```bash
user@pc zigbee2mqtt % enapter devices upload --blueprint-dir . --hardware-id REAL_UCM_ID
upload started with operation id 25721
[#25721] 2023-07-20T16:27:33Z [INFO] Started uploading blueprint[id=dcb05efe-1618-4b01-877b-6105960690bc] on device[hardware_id=REAL_UCM_ID]
[#25721] 2023-07-20T16:27:33Z [INFO] Generating configuration for uploading
[#25721] 2023-07-20T16:27:33Z [INFO] Updating configuration in the cloud platform
[#25721] 2023-07-20T16:27:33Z [INFO] Updating configuration on the gateway
[#25721] 2023-07-20T16:27:35Z [INFO] Uploading blueprint finished successfully
Done!
```

## Step 3. Configuring Standalone UCM

Open `docker-compose.yaml` in any editor.

Set environment variables according to your configuration settings. With dummy
settings your file will look like this:

```yaml
version: "3"
services:
  zigbee2mqtt-standalone:
    build: .
    image: enapter-standalone-examples/zigbee2mqtt:latest
    environment:
      - ENAPTER_STANDALONE_COMMUNICATION_CONFIG: "PUT_YOUR_CONFIG_HERE"
      - ZIGBEE_MQTT_HOST: "192.168.192.190"
      - ZIGBEE_MQTT_PORT: "9883"
      - ZIGBEE_MQTT_USER: "mqtt_user"
      - ZIGBEE_MQTT_PASSWORD: "mqtt_password"
      - ZIGBEE_MQTT_TOPIC: "zigbee2mqtt/MyDevice"
      - ZIGBEE_SENSOR_MANUFACTURER: "Device Manufacturer"
      - ZIGBEE_SENSOR_MODEL: "Device Model"
```

## Step 4. Build Docker Image with Standalone Device

> You can you can skip this step and go directly to Step 5. Docker Compose will
> automatically build your image before starting container.

Build your Docker image by running `bash docker_build.sh` command in directory
with Standalone Device.

```bash
user@pc zigbee2mqtt  % bash docker_build.sh
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load .dockerignore
#1 transferring context: 2B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 281B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.10-alpine3.16
#3 DONE 2.0s

#4 [1/7] FROM docker.io/library/python:3.10-alpine3.16@sha256:afe68972cc00883d70b3760ee0ffbb7375cf09706c122dda7063ffe64c5be21b
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 66B done
#5 DONE 0.0s

#6 [3/7] RUN apk add build-base
#6 CACHED

#7 [2/7] WORKDIR /app
#7 CACHED

#8 [4/7] RUN python -m venv .venv
#8 CACHED

#9 [5/7] COPY requirements.txt requirements.txt
#9 CACHED

#10 [6/7] RUN .venv/bin/pip install -r requirements.txt
#10 CACHED

#11 [7/7] COPY script.py script.py
#11 CACHED

#12 exporting to image
#12 exporting layers done
#12 writing image sha256:92e1050debeabaff5837c6ca5bc26b0b966d09fc6f24e21b1d10cbb2f4d9aeec done
#12 naming to docker.io/enapter-standalone-examples/zigbee2mqtt:latest done
#12 DONE 0.0s
```

Your `enapter-standalone-examples/zigbee2mqtt` image is now built and you can
see it by running `docker images` command:

```bash
user@pc zigbee2mqtt % docker images enapter-standalone-examples/zigbee2mqtt
REPOSITORY                                TAG       IMAGE ID       CREATED       SIZE
enapter-standalone-examples/zigbee2mqtt   latest    92e1050debea   5 hours ago   285MB
```

## Step 5. Run your Standalone Device Docker Container

Finally run your Standalone Device with `docker-compose up` command:

On this step you can check that your Device is now Online in the Cloud.
