import io
import pathlib
import zipfile

import httpx

from enapter.http import api

from .blueprint import Blueprint, BlueprintView


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def upload_file(self, path: pathlib.Path) -> Blueprint:
        with path.open("rb") as file:
            data = file.read()
        return await self.upload(data)

    async def upload_directory(self, path: pathlib.Path) -> Blueprint:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in path.rglob("*"):
                zip_file.write(file_path, arcname=file_path.relative_to(path))
        return await self.upload(buffer.getvalue())

    async def upload(self, data: bytes) -> Blueprint:
        url = "v3/blueprints/upload"
        response = await self._client.post(url, content=data)
        api.check_error(response)
        return Blueprint.from_dto(response.json()["blueprint"])

    async def download(
        self, blueprint_id: str, view: BlueprintView = BlueprintView.ORIGINAL
    ) -> bytes:
        url = f"v3/blueprints/{blueprint_id}/zip"
        response = await self._client.get(url, params={"view": view.value})
        api.check_error(response)
        return response.content
