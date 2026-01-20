import io
import pathlib
import zipfile

import httpx

from enapter.http import api

from .blueprint import Blueprint, BlueprintView


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get(self, blueprint_id: str) -> Blueprint:
        url = f"v3/blueprints/{blueprint_id}"
        response = await self._client.get(url)
        await api.check_error(response)
        return Blueprint.from_dto(response.json()["blueprint"])

    async def upload_file(self, path: pathlib.Path) -> Blueprint:
        with path.open("rb") as file:
            data = file.read()
        return await self.upload(data)

    async def upload_directory(self, path: pathlib.Path) -> Blueprint:
        data = await self._zip_directory(path)
        return await self.upload(data)

    async def upload(self, data: bytes) -> Blueprint:
        url = "v3/blueprints/upload"
        response = await self._client.post(url, content=data)
        await api.check_error(response)
        return Blueprint.from_dto(response.json()["blueprint"])

    async def download(
        self, blueprint_id: str, view: BlueprintView = BlueprintView.ORIGINAL
    ) -> bytes:
        url = f"v3/blueprints/{blueprint_id}/zip"
        response = await self._client.get(url, params={"view": view.value})
        await api.check_error(response)
        return response.content

    async def validate_file(self, path: pathlib.Path) -> None:
        with path.open("rb") as file:
            data = file.read()
        await self.validate(data)

    async def validate_directory(self, path: pathlib.Path) -> None:
        data = await self._zip_directory(path)
        await self.validate(data)

    async def validate(self, data: bytes) -> None:
        url = "v3/blueprints/validate"
        response = await self._client.post(url, content=data)
        await api.check_error(response)
        validation_errors = response.json().get("validation_errors", [])
        if validation_errors:
            raise api.MultiError(
                [api.Error(msg, code=None, details=None) for msg in validation_errors]
            )

    async def _zip_directory(self, path: pathlib.Path) -> bytes:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in path.rglob("*"):
                zip_file.write(file_path, arcname=file_path.relative_to(path))
        return buffer.getvalue()
