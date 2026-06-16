"""Unit tests for the authorization module."""

import pytest

import enapter


class TestAccessRole:
    """Tests for the AccessRole enum."""

    def test_all_members_exist(self):
        """Verify all expected AccessRole members are present and have correct string values."""
        assert enapter.http.api.AccessRole.READONLY.value == "READONLY"
        assert enapter.http.api.AccessRole.USER.value == "USER"
        assert enapter.http.api.AccessRole.OWNER.value == "OWNER"
        assert enapter.http.api.AccessRole.INSTALLER.value == "INSTALLER"
        assert enapter.http.api.AccessRole.SYSTEM.value == "SYSTEM"
        assert enapter.http.api.AccessRole.VENDOR.value == "VENDOR"

    def test_member_count(self):
        """Verify the enum has exactly 6 members."""
        assert len(enapter.http.api.AccessRole) == 6

    def test_has_docstring(self):
        """Verify the AccessRole enum carries a docstring."""
        assert enapter.http.api.AccessRole.__doc__ is not None

    @pytest.mark.parametrize(
        "value,expected_member",
        [
            ("READONLY", enapter.http.api.AccessRole.READONLY),
            ("USER", enapter.http.api.AccessRole.USER),
            ("OWNER", enapter.http.api.AccessRole.OWNER),
            ("INSTALLER", enapter.http.api.AccessRole.INSTALLER),
            ("SYSTEM", enapter.http.api.AccessRole.SYSTEM),
            ("VENDOR", enapter.http.api.AccessRole.VENDOR),
        ],
    )
    def test_construct_from_string(self, value, expected_member):
        """Verify AccessRole can be constructed from string values."""
        assert enapter.http.api.AccessRole(value) is expected_member
