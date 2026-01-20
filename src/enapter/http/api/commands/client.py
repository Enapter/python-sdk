from typing import AsyncGenerator

import httpx

from enapter import async_
from enapter.http import api

from .execution import Execution, ListExecutionsOrder


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_execution(
        self, device_id: str, execution_id: str, expand_log: bool = False
    ) -> Execution:
        url = f"v3/devices/{device_id}/command_executions/{execution_id}"
        expand = {"log": expand_log}
        expand_string = ",".join(k for k, v in expand.items() if v)
        response = await self._client.get(url, params={"expand": expand_string})
        await api.check_error(response)
        return Execution.from_dto(response.json()["execution"])

    @async_.generator
    async def list_executions(
        self,
        device_id: str,
        order: ListExecutionsOrder = ListExecutionsOrder.CREATED_AT_ASC,
    ) -> AsyncGenerator[Execution, None]:
        url = f"v3/devices/{device_id}/command_executions"
        limit = 50
        offset = 0
        while True:
            response = await self._client.get(
                url, params={"order": order.value, "limit": limit, "offset": offset}
            )
            await api.check_error(response)
            payload = response.json()
            if not payload["executions"]:
                return
            for dto in payload["executions"]:
                yield Execution.from_dto(dto)
            offset += limit

    async def execute(
        self,
        device_id: str,
        name: str,
        arguments: dict | None = None,
        expand_log: bool = False,
    ) -> Execution:
        url = f"v3/devices/{device_id}/execute_command"
        expand = {"log": expand_log}
        expand_string = ",".join(k for k, v in expand.items() if v)
        if arguments is None:
            arguments = {}
        response = await self._client.post(
            url,
            params={"expand": expand_string},
            json={"name": name, "arguments": arguments},
        )
        await api.check_error(response)
        return Execution.from_dto(response.json()["execution"])

    async def create_execution(
        self, device_id: str, name: str, arguments: dict | None = None
    ) -> Execution:
        url = f"v3/devices/{device_id}/command_executions"
        if arguments is None:
            arguments = {}
        response = await self._client.post(
            url, json={"name": name, "arguments": arguments}
        )
        await api.check_error(response)
        return await self.get_execution(
            device_id=device_id, execution_id=response.json()["execution_id"]
        )
