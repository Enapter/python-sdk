import os
from typing import MutableMapping, Self


class TLSConfig:

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

    def __init__(self, secret_key: str, cert: str, ca_cert: str) -> None:
        self.secret_key = secret_key
        self.cert = cert
        self.ca_cert = ca_cert


class Config:

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self:
        prefix = namespace + "MQTT_API_"
        return cls(
            host=env[prefix + "HOST"],
            port=int(env[prefix + "PORT"]),
            user=env.get(prefix + "USER", default=None),
            password=env.get(prefix + "PASSWORD", default=None),
            tls_config=TLSConfig.from_env(env, namespace=namespace),
        )

    def __init__(
        self,
        host: str,
        port: int,
        user: str | None = None,
        password: str | None = None,
        tls_config: TLSConfig | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.tls_config = tls_config

    @property
    def tls(self) -> TLSConfig | None:
        return self.tls_config

    def __repr__(self) -> str:
        return "mqtt.api.Config(host=%r, port=%r, tls=%r)" % (
            self.host,
            self.port,
            self.tls is not None,
        )
