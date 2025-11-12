import asyncio
import os
import socket
from typing import AsyncGenerator, Generator

import docker
import docker.models.containers
import pytest

import enapter

MOSQUITTO_PORT = "1883/tcp"


@pytest.fixture(name="enapter_mqtt_client")
async def fixture_enapter_mqtt_client(
    mosquitto_container: docker.models.containers.Container,
) -> AsyncGenerator[enapter.mqtt.Client, None]:
    ports = mosquitto_container.ports[MOSQUITTO_PORT]
    assert ports
    async with asyncio.TaskGroup() as tg:
        async with enapter.mqtt.Client(
            hostname=ports[0]["HostIp"],
            port=int(ports[0]["HostPort"]),
            task_group=tg,
        ) as mqtt_client:
            yield mqtt_client


@pytest.fixture(scope="session", name="mosquitto_container")
def fixture_mosquitto_container(
    docker_client: docker.DockerClient,
) -> Generator[docker.models.containers.Container, None]:
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


def random_unused_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        return addr[1]


@pytest.fixture(name="docker_client", scope="session")
def fixture_docker_client() -> Generator[docker.DockerClient, None]:
    docker_client = docker.from_env()
    try:
        yield docker_client
    finally:
        docker_client.close()
