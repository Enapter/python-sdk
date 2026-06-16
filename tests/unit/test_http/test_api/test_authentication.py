"""Unit tests for the HTTP API authentication scheme."""

import httpx

from enapter.http.api.authentication import AuthenticationScheme


def test_authentication_scheme_is_httpx_auth_subclass():
    """AuthenticationScheme must subclass httpx.Auth."""
    assert issubclass(AuthenticationScheme, httpx.Auth)


def test_authentication_scheme_sets_token_header():
    """AuthenticationScheme must set the X-Enapter-Auth-Token header when a token is provided."""
    scheme = AuthenticationScheme(token="test_token")
    request = next(scheme.auth_flow(httpx.Request("GET", "https://api.enapter.com/")))
    assert request.headers["X-Enapter-Auth-Token"] == "test_token"


def test_authentication_scheme_sets_user_header():
    """AuthenticationScheme must set the X-Enapter-Auth-User header when a user is provided."""
    scheme = AuthenticationScheme(user="test_user")
    request = next(scheme.auth_flow(httpx.Request("GET", "https://api.enapter.com/")))
    assert request.headers["X-Enapter-Auth-User"] == "test_user"


def test_authentication_scheme_sets_both_headers():
    """AuthenticationScheme must set both headers when both token and user are provided."""
    scheme = AuthenticationScheme(token="test_token", user="test_user")
    request = next(scheme.auth_flow(httpx.Request("GET", "https://api.enapter.com/")))
    assert request.headers["X-Enapter-Auth-Token"] == "test_token"
    assert request.headers["X-Enapter-Auth-User"] == "test_user"


def test_authentication_scheme_omits_headers_when_none():
    """AuthenticationScheme must not set headers when token/user are None."""
    scheme = AuthenticationScheme()
    request = next(scheme.auth_flow(httpx.Request("GET", "https://api.enapter.com/")))
    assert "X-Enapter-Auth-Token" not in request.headers
    assert "X-Enapter-Auth-User" not in request.headers
