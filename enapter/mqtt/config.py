import os


class Config:
    @classmethod
    def from_env(cls, prefix="ENAPTER_", env=os.environ):
        def pem(value):
            if value is None:
                return value
            return value.replace("\\n", "\n")

        return cls(
            host=env[prefix + "MQTT_HOST"],
            port=int(env[prefix + "MQTT_PORT"]),
            user=env.get(prefix + "MQTT_USER", default=None),
            password=env.get(prefix + "MQTT_PASSWORD", default=None),
            tls_secret_key=pem(env.get(prefix + "MQTT_TLS_SECRET_KEY", default=None)),
            tls_cert=pem(env.get(prefix + "MQTT_TLS_CERT", default=None)),
            tls_ca_cert=pem(env.get(prefix + "MQTT_TLS_CA_CERT", default=None)),
        )

    def __init__(
        self,
        host,
        port,
        user=None,
        password=None,
        tls_secret_key=None,
        tls_cert=None,
        tls_ca_cert=None,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.tls_secret_key = tls_secret_key
        self.tls_cert = tls_cert
        self.tls_ca_cert = tls_ca_cert

        self.tls_enabled = {tls_secret_key, tls_cert, tls_ca_cert} != {None}

    def __repr__(self):
        return "mqtt.Config(host=%r, port=%r, tls_enabled=%r)" % (
            self.host,
            self.port,
            self.tls_enabled,
        )
