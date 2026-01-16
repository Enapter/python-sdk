import enapter


class TestServer:

    async def test_ping(self) -> None:
        host = "127.0.0.1"
        # FIXME: Hard-code.
        port = 12345
        async with enapter.mcp.Server(host=host, port=port, http_api_base_url=""):
            async with enapter.mcp.Client(url=f"http://{host}:{port}/mcp") as client:
                assert await client.ping()
