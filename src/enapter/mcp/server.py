from typing import AsyncContextManager

import fastmcp

from enapter import async_, http


class Server(async_.Routine):

    def __init__(self, host: str, port: int, http_api_base_url: str) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._http_api_base_url = http_api_base_url

    async def _run(self) -> None:
        mcp = fastmcp.FastMCP()
        self._register_tools(mcp)
        await mcp.run_async(
            transport="streamable-http",
            show_banner=False,
            host=self._host,
            port=self._port,
        )

    def _register_tools(self, mcp: fastmcp.FastMCP) -> None:
        mcp.tool(
            self._list_sites,
            name="list_sites",
            description="List all sites to which the authenticated user has access.",
        )
        mcp.tool(
            self._get_site,
            name="get_site",
            description="Get site by ID.",
        )
        mcp.tool(
            self._list_devices,
            name="list_devices",
            description="List devices.",
        )
        mcp.tool(
            self._get_device,
            name="get_device",
            description="Get device by ID.",
        )
        mcp.tool(
            self._get_latest_telemetry,
            name="get_latest_telemetry",
            description="Get latest telemetry of multiple devices.",
        )

    async def _list_sites(self) -> list:
        async with self._new_http_api_client() as client:
            async with client.sites.list() as stream:
                return [site.to_dto() async for site in stream]

    async def _get_site(self, site_id: str) -> dict:
        async with self._new_http_api_client() as client:
            site = await client.sites.get(site_id)
            return site.to_dto()

    async def _list_devices(
        self,
        expand_manifest: bool = False,
        expand_properties: bool = False,
        expand_connectivity: bool = False,
        site_id: str | None = None,
    ) -> list:
        async with self._new_http_api_client() as client:
            async with client.devices.list(
                expand_manifest=expand_manifest,
                expand_properties=expand_properties,
                expand_connectivity=expand_connectivity,
                site_id=site_id,
            ) as stream:
                return [device.to_dto() async for device in stream]

    async def _get_device(
        self,
        device_id: str,
        expand_manifest: bool = False,
        expand_properties: bool = False,
        expand_connectivity: bool = False,
    ) -> dict:
        async with self._new_http_api_client() as client:
            device = await client.devices.get(
                device_id,
                expand_manifest=expand_manifest,
                expand_properties=expand_properties,
                expand_connectivity=expand_connectivity,
            )
            return device.to_dto()

    async def _get_latest_telemetry(
        self, attributes_by_device: dict[str, list[str]]
    ) -> dict[str, dict[str, str | int | float | None]]:
        async with self._new_http_api_client() as client:
            telemetry = await client.telemetry.latest(attributes_by_device)
            return {
                device: {
                    attribute: datapoint.to_dto() if datapoint is not None else None  # type: ignore
                    for attribute, datapoint in attributes.items()
                }
                for device, attributes in telemetry.items()
            }

    def _new_http_api_client(self) -> AsyncContextManager[http.api.Client]:
        # FIXME: Client instance gets created for each request.
        headers = fastmcp.server.dependencies.get_http_headers()
        token = headers["x-enapter-auth-token"]
        return http.api.Client(
            config=http.api.Config(token=token, base_url=self._http_api_base_url)
        )
