import os


class Config:
    @classmethod
    def from_env(cls, prefix="ENAPTER_", env=os.environ):
        not_specified = object()

        def get(var, default=not_specified):
            try:
                return env[prefix + "MQTT_" + var]
            except KeyError:
                if default is not_specified:
                    raise
                return default

        def get_pem(*args, **kwargs):
            value = get(*args, **kwargs)
            if value is not None:
                value = value.replace("\\n", "\n")
            return value

        return cls(
            host=get("HOST"),
            port=int(get("PORT")),
            user=get("USER", default=None),
            password=get("PASSWORD", default=None),
            tls_secret_key=get_pem("TLS_SECRET_KEY", default=None),
            tls_cert=get_pem("TLS_CERT", default=None),
            tls_ca_cert=get_pem("TLS_CA_CERT", default=None),
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
