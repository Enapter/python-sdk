import os
from typing import MutableMapping, Optional


class TLSConfig:

    @classmethod
    def from_env(
        cls, prefix: str = "ENAPTER_", env: MutableMapping[str, str] = os.environ
    ) -> Optional["TLSConfig"]:
        secret_key = env.get(prefix + "MQTT_TLS_SECRET_KEY")
        cert = env.get(prefix + "MQTT_TLS_CERT")
        ca_cert = env.get(prefix + "MQTT_TLS_CA_CERT")

        nothing_defined = {secret_key, cert, ca_cert} == {None}
        if nothing_defined:
            return None

        if secret_key is None:
            raise KeyError(prefix + "MQTT_TLS_SECRET_KEY")
        if cert is None:
            raise KeyError(prefix + "MQTT_TLS_CERT")
        if ca_cert is None:
            raise KeyError(prefix + "MQTT_TLS_CA_CERT")

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
        cls, prefix: str = "ENAPTER_", env: MutableMapping[str, str] = os.environ
    ) -> "Config":
        return cls(
            host=env[prefix + "MQTT_HOST"],
            port=int(env[prefix + "MQTT_PORT"]),
            user=env.get(prefix + "MQTT_USER", default=None),
            password=env.get(prefix + "MQTT_PASSWORD", default=None),
            tls=TLSConfig.from_env(prefix=prefix, env=env),
        )

    def __init__(
        self,
        host: str,
        port: int,
        user: Optional[str] = None,
        password: Optional[str] = None,
        tls: Optional[TLSConfig] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.tls = tls

    def __repr__(self) -> str:
        return "mqtt.Config(host=%r, port=%r, tls=%r)" % (
            self.host,
            self.port,
            self.tls is not None,
        )
