import dns.asyncresolver


class Resolver:
    def __init__(self, nameservers=("224.0.0.251",), port=5353, timeout=4, lifetime=10):
        self._resolver = dns.asyncresolver.Resolver()
        self._resolver.nameservers = list(nameservers)
        self._resolver.port = port
        self._resolver.timeout = timeout
        self._resolver.lifetime = lifetime

    async def resolve(self, host):
        answer = await self._resolver.resolve(host, "A")
        if not answer:
            raise ValueError(f"empty answer received: {host}")

        return answer[0].address
