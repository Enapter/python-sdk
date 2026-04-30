import datetime
from typing import AsyncContextManager, AsyncGenerator, List

import httpx

from enapter.http import api

from .execution import Execution, ExecutionState, ListExecutionsOrder


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

    def list_executions(
        self,
        device_id: str | None = None,
        site_id: str | None = None,
        order: ListExecutionsOrder = ListExecutionsOrder.CREATED_AT_ASC,
        created_at_gte: datetime.datetime | None = None,
        created_at_lt: datetime.datetime | None = None,
        state: ExecutionState | list[ExecutionState] | None = None,
        name: str | list[str] | None = None,
        offset: int = 0,
        limit: int | None = None,
    ) -> AsyncContextManager[AsyncGenerator[Execution, None]]:
        async def fetch_page(query: api.PageQuery) -> List[Execution]:
            return await self._list_executions(
                device_id=device_id,
                site_id=site_id,
                order=order,
                created_at_gte=created_at_gte,
                created_at_lt=created_at_lt,
                state=state,
                name=name,
                offset=query.offset,
                limit=query.limit,
            )

        return api.paginate(fetch_page, chunk_size=50, offset=offset, limit=limit)

    async def _list_executions(
        self,
        device_id: str | None,
        site_id: str | None,
        order: ListExecutionsOrder,
        created_at_gte: datetime.datetime | None,
        created_at_lt: datetime.datetime | None,
        state: ExecutionState | list[ExecutionState] | None,
        name: str | list[str] | None,
        offset: int,
        limit: int,
    ) -> List[Execution]:
        params = {"order": order.value}

        if created_at_gte is not None:
            params["created_at.gte"] = created_at_gte.isoformat()

        if created_at_lt is not None:
            params["created_at.lt"] = created_at_lt.isoformat()

        if state is not None:
            if isinstance(state, ExecutionState):
                state = [state]
            params["state.in"] = ",".join(s.value for s in state)

        if name is not None:
            if isinstance(name, str):
                name = [name]
            params["name.in"] = ",".join(name)

        if site_id is not None:
            url = f"v3/sites/{site_id}/commands/executions"
            if device_id is not None:
                params["device_id.in"] = device_id
        elif device_id is not None:
            url = f"v3/devices/{device_id}/command_executions"
        else:
            raise ValueError("either device_id or site_id must be provided")

        response = await self._client.get(
            url, params={**params, "offset": offset, "limit": limit}
        )
        await api.check_error(response)
        payload = response.json()
        return [Execution.from_dto(dto) for dto in payload.get("executions", [])]

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
