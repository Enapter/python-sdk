# SPEC-002: Introduce `authorization.py` and Move `AuthorizedRole`

## Context

`AuthorizedRole` currently lives under `enapter.http.api.devices`, even though the HTTP API returns `authorized_role` on both Device and Site resources. The enum describes a cross-resource authorization concept and deserves a first-class home in the `http.api` package.

## Architectural Decisions

1. **Create `enapter.http.api.authorization` as the canonical home for authorization primitives.**
   `AuthorizedRole` moves from `enapter.http.api.devices.authorized_role` to `enapter.http.api.authorization`.

2. **Export `AuthorizedRole` from `enapter.http.api`.**
   The public import path becomes `enapter.http.api.AuthorizedRole`.

3. **Do not preserve a backward-compatible export from `enapter.http.api.devices`.**
   This is an intentional breaking change. Callers must update their imports.

4. **Do not change enum values.**
   The real API returns `READONLY` (no underscore), which the enum already supports. The public documentation will be corrected out-of-band.

5. **Keep `SYSTEM`.**
   It is an intentionally undocumented hidden role used by the API. Removing it would break existing consumers.

## Requirements

1. Create `src/enapter/http/api/authorization.py` containing the `AuthorizedRole` enum with the existing members:
   - `READONLY = "READONLY"`
   - `USER = "USER"`
   - `OWNER = "OWNER"`
   - `INSTALLER = "INSTALLER"`
   - `SYSTEM = "SYSTEM"`
   - `VENDOR = "VENDOR"`

2. Export `AuthorizedRole` from `src/enapter/http/api/__init__.py`.

3. Remove `src/enapter/http/api/devices/authorized_role.py` and the `AuthorizedRole` export from `src/enapter/http/api/devices/__init__.py`.

4. Update `src/enapter/http/api/devices/device.py` to use `AuthorizedRole` via `from enapter.http import api` and `api.AuthorizedRole`, matching the pattern already used in `devices/client.py`.

5. Update `tests/unit/test_http/test_api/test_devices/test_client.py` and any other tests that import `AuthorizedRole` from `enapter.http.api.devices` to use the new path.

6. Add or keep a dedicated test that asserts all `AuthorizedRole` members and their string values.

## Constraints

- Do **not** rename, add, or remove enum members.
- Do **not** change `Device` field set or semantics.
- Do **not** add `authorized_role` to `Site` in this change.

## Acceptance Criteria

- `enapter.http.api.AuthorizedRole` is importable and exposes all expected members.
- `pytest tests/unit/test_http/test_api/test_devices` passes.
- `pytest tests/unit/test_http/test_api/test_client` passes.
- A codebase-wide search for `enapter.http.api.devices.AuthorizedRole` returns no references.
- All existing tests continue to pass.
