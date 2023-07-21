# Eaton UPS Standalone UCM (SNMP)

This example describes the implementation of the [Standalone UCM](https://handbook.enapter.com/software/virtual_ucm/) concept using the opensource [Enapter python-sdk](https://github.com/Enapter/python-sdk) for monitoring Eaton UPS using SNMP protocol.

In order to use this UCM you need to enable SNMPv1 protocol in the Web Interface of your UPS and set unique community name for the read only access. The default port for SNMP is 161 but also can be changed.

As an example in this guide we will use the following dummy settings for configuration:

UPS IP Address: 192.168.192.192

Community Name: public

SNMP Port: 161

## Requirements

It is recommended to run this UCM using Docker and Docker Compose. This will ensure that environment is correct.

The UPS must be reachable from the computer where the Docker Container will be running. You can check availability and settings with `snmpget` command on Linux or Mac:

```bash
user@pc snmp-eaton-ups % snmpget -v1 -c public 192.168.192.192:161 1.3.6.1.2.1.33.1.1.1.0
SNMPv2-SMI::mib-2.33.1.1.1.0 = STRING: "EATON"
```

## Step 1. Create Standalone UCM in Enapter Cloud

Log in to the Enapter Cloud, navigate to the Site where you want to create Standalone UCM and click on `Add new` button in the Standalone Device section.

After creating Standalone UCM, you need to Generate and save Configuration string also known as ENAPTER_VUCM_BLOB as well as save UCM ID which will be needed for the next step

More information you can find on [this page](https://developers.enapter.com/docs/tutorial/software-ucms/standalone).

## Step 2. Upload Blueprint into the Cloud

The general case [Enapter Blueprint](https://marketplace.enapter.com/about) consists of two files - declaration in YAML format (manifest.yaml) and logic written in Lua. Howerver for this case the logic is written in Python as Lua implementation doesn't have SNMP integration.

But for both cases we need to tell Enapter Cloud which telemetry we are going to send and store and how to name it.

The easiest way to do that - using [Enapter CLI](https://github.com/Enapter/enapter-cli) to upload manifest.yaml into Cloud. The other option is to use [Web IDE](https://developers.enapter.com/docs/tutorial/uploading-blueprint).

```bash
user@pc snmp-eaton-ups % enapter devices upload --blueprint-dir . --hardware-id REAL_UCM_ID
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

Set environment variables according to your configuration settings. With dummy settings your file will look like this:

```yaml
version: "3"
services:
  snmp-eaton-ups-ucm:
    build: .
    image: enapter-vucm-examples/snmp-eaton-ups:latest
    environment:
      - "ENAPTER_VUCM_BLOB=REALENAPTERVUCMBLOBMUSTBEHERE="
      - "ENAPTER_SNMP_HOST=192.168.192.192"
      - "ENAPTER_SNMP_PORT=161"
      - "ENAPTER_SNMP_COMMUNITY=public"
```

## Step 4. Build Docker Image with Standalone UCM

> You can you can skip this step and go directly to th Step 5.
> Docker Compose will automatically build your image before starting container.

Build your Docker image by running `bash docker_build.sh` command in directory with UCM.

```bash
user@pc snmp-eaton-ups % bash docker_build.sh
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
#12 naming to docker.io/enapter-vucm-examples/snmp-eaton-ups:latest done
#12 DONE 0.0s
```

Your `enapter-vucm-examples/snmp-eaton-ups` image is now built and you can see it by running `docker images` command:

```bash
user@pc snmp-eaton-ups % docker images enapter-vucm-examples/snmp-eaton-ups
REPOSITORY                             TAG       IMAGE ID       CREATED       SIZE
enapter-vucm-examples/snmp-eaton-ups   latest    92e1050debea   5 hours ago   285MB
```

## Step 5. Run your Standalone UCM Docker Container

Finally run your Standalone UCM with `docker-compose up` command:

```bash
user@pc snmp-eaton-ups % docker-compose up
[+] Running 1/0
 ✔ Container snmp-eaton-ups-snmp-eaton-ups-ucm-1  Created                                                                                                            0.0s
Attaching to snmp-eaton-ups-snmp-eaton-ups-ucm-1
snmp-eaton-ups-snmp-eaton-ups-ucm-1  | {"time": "2023-07-20T15:50:01.570744", "level": "INFO", "name": "enapter.mqtt.client", "host": "10.1.1.47", "port": 8883, "message": "starting"}
snmp-eaton-ups-snmp-eaton-ups-ucm-1  | {"time": "2023-07-20T15:50:21.776037", "level": "INFO", "name": "enapter.mqtt.client", "host": "10.1.1.47", "port": 8883, "message": "client ready"}
```

On this step you can check that your UCM is now Online in the Cloud.
