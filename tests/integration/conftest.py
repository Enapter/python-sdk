import os
import socket

import docker
import pytest

import enapter

MOSQUITTO_PORT = "1883/tcp"


@pytest.fixture(name="enapter_mqtt_client")
async def fixture_enapter_mqtt_client(mosquitto_container):
    ports = mosquitto_container.ports[MOSQUITTO_PORT]
    assert ports

    config = enapter.mqtt.Config(
        host=ports[0]["HostIp"],
        port=int(ports[0]["HostPort"]),
    )
    async with enapter.mqtt.Client(config) as mqtt_client:
        yield mqtt_client


@pytest.fixture(scope="session", name="mosquitto_container")
def fixture_mosquitto_container(docker_client):
    name = "enapter-python-sdk-integration-tests-mosquitto"

    try:
        old_mosquitto = docker_client.containers.get(name)
    except docker.errors.NotFound:
        pass
    else:
        old_mosquitto.remove(force=True)

    mosquitto = docker_client.containers.run(
        os.getenv("MOSQUITTO_IMAGE", "eclipse-mosquitto:latest"),
        ["mosquitto", "-c", "/mosquitto-no-auth.conf"],
        name=name,
        network="bridge",
        ports={MOSQUITTO_PORT: ("127.0.0.1", random_unused_port())},
        detach=True,
        remove=True,
    )
    try:
        mosquitto.reload()
        yield mosquitto
    finally:
        mosquitto.stop()


def random_unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        return addr[1]


@pytest.fixture(name="docker_client", scope="session")
def fixture_docker_client():
    docker_client = docker.from_env()
    try:
        yield docker_client
    finally:
        docker_client.close()
