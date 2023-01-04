import random

import faker


class FakeDataGenerator:
    def __init__(self, seed: int):
        self._random = random.Random(seed)
        self._fake = self._new_faker(seed)

    def timestamp(self) -> int:
        dt = self._fake.date_time_this_month()
        return int(dt.timestamp())

    def hardware_id(self) -> str:
        n = self._random.getrandbits(20 * 8)
        return hex(n)[2:].upper()

    def channel_id(self) -> str:
        return self._fake.word()

    def _new_faker(self, seed):
        fake = faker.Faker()
        fake.seed_instance(seed)
        return fake
