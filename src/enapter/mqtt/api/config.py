import dataclasses
import os
from typing import MutableMapping, Self


@dataclasses.dataclass(repr=False)
class TLSConfig:

    secret_key: str
    cert: str
    ca_cert: str

    def __repr__(self) -> str:
        return "mqtt.api.TLSConfig(...)"

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self | None:
        prefix = namespace + "MQTT_API_TLS_"

        secret_key = env.get(prefix + "SECRET_KEY")
        cert = env.get(prefix + "CERT")
        ca_cert = env.get(prefix + "CA_CERT")

        nothing_defined = {secret_key, cert, ca_cert} == {None}
        if nothing_defined:
            return None

        if secret_key is None:
            raise KeyError(prefix + "SECRET_KEY")
        if cert is None:
            raise KeyError(prefix + "CERT")
        if ca_cert is None:
            raise KeyError(prefix + "CA_CERT")

        def pem(value: str) -> str:
            return value.replace("\\n", "\n")

        return cls(secret_key=pem(secret_key), cert=pem(cert), ca_cert=pem(ca_cert))


@dataclasses.dataclass
class Config:

    host: str
    port: int
    user: str | None = None
    password: str | None = None
    tls_config: TLSConfig | None = None

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self:
        prefix = namespace + "MQTT_API_"
        return cls(
            host=env[prefix + "HOST"],
            port=int(env[prefix + "PORT"]),
            user=env.get(prefix + "USER", None),
            password=env.get(prefix + "PASSWORD", None),
            tls_config=TLSConfig.from_env(env, namespace=namespace),
        )

    @property
    def tls(self) -> TLSConfig | None:
        return self.tls_config
