"""Unit tests for the authorization module."""

import pytest

import enapter


class TestAuthorizedRole:
    """Tests for the AuthorizedRole enum."""

    def test_all_members_exist(self):
        """Verify all expected AuthorizedRole members are present and have correct string values."""
        assert enapter.http.api.AuthorizedRole.READONLY.value == "READONLY"
        assert enapter.http.api.AuthorizedRole.USER.value == "USER"
        assert enapter.http.api.AuthorizedRole.OWNER.value == "OWNER"
        assert enapter.http.api.AuthorizedRole.INSTALLER.value == "INSTALLER"
        assert enapter.http.api.AuthorizedRole.SYSTEM.value == "SYSTEM"
        assert enapter.http.api.AuthorizedRole.VENDOR.value == "VENDOR"

    def test_member_count(self):
        """Verify the enum has exactly 6 members."""
        assert len(enapter.http.api.AuthorizedRole) == 6

    @pytest.mark.parametrize(
        "value,expected_member",
        [
            ("READONLY", enapter.http.api.AuthorizedRole.READONLY),
            ("USER", enapter.http.api.AuthorizedRole.USER),
            ("OWNER", enapter.http.api.AuthorizedRole.OWNER),
            ("INSTALLER", enapter.http.api.AuthorizedRole.INSTALLER),
            ("SYSTEM", enapter.http.api.AuthorizedRole.SYSTEM),
            ("VENDOR", enapter.http.api.AuthorizedRole.VENDOR),
        ],
    )
    def test_construct_from_string(self, value, expected_member):
        """Verify AuthorizedRole can be constructed from string values."""
        assert enapter.http.api.AuthorizedRole(value) is expected_member
