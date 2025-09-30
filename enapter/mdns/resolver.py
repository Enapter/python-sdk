import logging

import dns.asyncresolver  # type: ignore

LOGGER = logging.getLogger(__name__)


class Resolver:
    def __init__(self) -> None:
        self._logger = LOGGER
        self._dns_resolver = self._new_dns_resolver()
        self._mdns_resolver = self._new_mdns_resolver()

    async def resolve(self, host: str) -> str:
        # TODO: Resolve concurrently.
        try:
            ip = await self._resolve(self._dns_resolver, host)
            self._logger.debug("%r resolved using DNS: %r", host, ip)
            return ip
        except Exception as e:
            self._logger.debug(
                "switching to mDNS: failed to resolve %r using DNS: %r", host, e
            )
            ip = await self._resolve(self._mdns_resolver, host)
            self._logger.info("%r resolved using mDNS: %r", host, ip)
            return ip

    async def _resolve(self, resolver: dns.asyncresolver.Resolver, host: str) -> str:
        answer = await resolver.resolve(host, "A")
        if not answer:
            raise ValueError(f"empty answer received: {host}")

        return answer[0].address

    def _new_dns_resolver(self) -> dns.asyncresolver.Resolver:
        return dns.asyncresolver.Resolver(configure=True)

    def _new_mdns_resolver(self) -> dns.asyncresolver.Resolver:
        r = dns.asyncresolver.Resolver(configure=False)
        r.nameservers = ["224.0.0.251"]
        r.port = 5353
        return r
