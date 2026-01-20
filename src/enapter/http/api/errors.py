from typing import Any, Self

import httpx


async def check_error(response: httpx.Response) -> None:
    if not response.is_success:
        await response.aread()
        try:
            dto = response.json()
        except Exception:
            response.raise_for_status()
        MultiError.from_dto(dto).raise_()


class Error(Exception):

    def __init__(self, message: str, code: str | None, details: dict | None) -> None:
        self.message = message
        self.code = code
        self.details = details
        super().__init__(f"{message} (code={code}, details={details})")

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            message=dto.get("message", "<no message>"),
            code=dto.get("code"),
            details=dto.get("details"),
        )


class MultiError(Exception):

    def __init__(self, errors: list[Error]) -> None:
        self.errors = errors
        messages = "; ".join(repr(err) for err in errors)
        super().__init__(messages)

    def raise_(self) -> None:
        if len(self.errors) == 1:
            raise self.errors[0]
        raise self

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        errors = dto["errors"]
        if not errors:
            raise ValueError("empty error list")
        return cls(errors=[Error.from_dto(err) for err in errors])
