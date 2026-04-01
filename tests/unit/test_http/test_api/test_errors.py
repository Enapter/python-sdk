import httpx
import pytest

from enapter.http.api.errors import Error, MultiError, check_error


@pytest.mark.asyncio
async def test_check_error_success():
    """Test that check_error does nothing when response is successful."""
    response = httpx.Response(status_code=200, request=httpx.Request("GET", "https://example.com"))
    await check_error(response)


@pytest.mark.asyncio
async def test_check_error_non_json():
    """Test that check_error calls raise_for_status when response is not JSON."""
    response = httpx.Response(status_code=500, content=b"Internal Server Error", request=httpx.Request("GET", "https://example.com"))
    with pytest.raises(httpx.HTTPStatusError):
        await check_error(response)


@pytest.mark.asyncio
async def test_check_error_api_error_single():
    """Test that check_error raises a single Error when one is present in DTO."""
    dto = {
        "errors": [
            {
                "message": "Device not found",
                "code": "DEVICE_NOT_FOUND",
                "details": {"device_id": "test_device"},
            }
        ]
    }
    response = httpx.Response(status_code=404, json=dto, request=httpx.Request("GET", "https://example.com"))
    with pytest.raises(Error) as exc_info:
        await check_error(response)

    assert exc_info.value.message == "Device not found"
    assert exc_info.value.code == "DEVICE_NOT_FOUND"
    assert exc_info.value.details == {"device_id": "test_device"}


@pytest.mark.asyncio
async def test_check_error_api_error_multiple():
    """Test that check_error raises MultiError when multiple are present in DTO."""
    dto = {
        "errors": [
            {"message": "Invalid parameter A", "code": "INVALID_PARAM"},
            {"message": "Invalid parameter B", "code": "INVALID_PARAM"},
        ]
    }
    response = httpx.Response(status_code=400, json=dto, request=httpx.Request("GET", "https://example.com"))
    with pytest.raises(MultiError) as exc_info:
        await check_error(response)

    assert len(exc_info.value.errors) == 2
    assert exc_info.value.errors[0].message == "Invalid parameter A"
    assert exc_info.value.errors[1].message == "Invalid parameter B"


def test_error_from_dto_empty():
    """Test Error.from_dto with minimal fields."""
    err = Error.from_dto({})
    assert err.message == "<no message>"
    assert err.code is None
    assert err.details is None


def test_multi_error_from_dto_empty_list():
    """Test MultiError.from_dto raises ValueError on empty error list."""
    with pytest.raises(ValueError, match="empty error list"):
        MultiError.from_dto({"errors": []})
