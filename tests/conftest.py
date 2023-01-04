import os
import time

import pytest

from .fake_data_generator import FakeDataGenerator


@pytest.fixture(name="fake", scope="session")
def fixture_fake_data_generator():
    """A fixture that returns an instance of a fake data generator."""
    seed = int(os.getenv("FAKE_DATA_GENERATOR_SEED", time.time()))
    print(f"fake data generator seed: {seed}")
    return FakeDataGenerator(seed=seed)
