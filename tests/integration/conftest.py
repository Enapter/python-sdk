import asyncio
import os
import socket
from typing import AsyncGenerator, Generator

import docker
import docker.models.containers
import pytest

import enapter

MOSQUITTO_PORT = "1883/tcp"
# Timeout for Docker image pull operations (in seconds)
DOCKER_PULL_TIMEOUT = 300  # 5 minutes


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
) -> Generator[docker.models.containers.Container, None, None]:
    name = "enapter-python-sdk-integration-tests-mosquitto"
    image = os.getenv("MOSQUITTO_IMAGE", "eclipse-mosquitto:latest")

    # Ensure the image is available locally
    try:
        docker_client.images.get(image)
    except docker.errors.ImageNotFound:
        # Pull the image if not available locally
        # This is handled by the CI workflow, but we keep it here for local testing
        pull_docker_image_with_timeout(docker_client, image)
    except docker.errors.APIError as e:
        raise RuntimeError(
            f"Failed to access Docker daemon or image {image}. "
            f"Please ensure Docker is running. Error: {e}"
        ) from e

    try:
        old_mosquitto = docker_client.containers.get(name)
    except docker.errors.NotFound:
        pass
    else:
        old_mosquitto.remove(force=True)

    mosquitto = docker_client.containers.run(
        image,
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


def pull_docker_image_with_timeout(
    docker_client: docker.DockerClient, image: str, timeout: int = DOCKER_PULL_TIMEOUT
) -> None:
    """Pull a Docker image with a timeout.

    Args:
        docker_client: Docker client instance
        image: Image name to pull
        timeout: Timeout in seconds (default: DOCKER_PULL_TIMEOUT)

    Raises:
        RuntimeError: If the image pull fails or times out
        TimeoutError: If the operation exceeds the timeout
    """
    import concurrent.futures

    def _pull_image() -> None:
        try:
            docker_client.images.pull(image)
        except docker.errors.APIError as e:
            raise RuntimeError(
                f"Failed to pull Docker image {image}. "
                f"Please ensure Docker is running and you have network connectivity. "
                f"Error: {e}"
            ) from e

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_pull_image)
        try:
            future.result(timeout=timeout)
        except concurrent.futures.TimeoutError as e:
            raise TimeoutError(
                f"Timeout while pulling Docker image {image} after {timeout} seconds. "
                f"Please check your network connection or increase the timeout."
            ) from e
        except Exception:
            # Re-raise any other exceptions from the pull operation
            raise


@pytest.fixture(name="docker_client", scope="session")
def fixture_docker_client() -> Generator[docker.DockerClient, None, None]:
    docker_client = docker.from_env()
    try:
        yield docker_client
    finally:
        docker_client.close()
