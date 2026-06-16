# SPEC-003: Add `authorized_role` to `Site`

## Context

The Enapter HTTP API returns `authorized_role` on every [Site](https://v3.developers.enapter.com/reference/http/sites) resource, but the SDK's `Site` model does not parse or expose it. After `AuthorizedRole` is moved to `enapter.http.api.authorization` (SPEC-002), it can be reused for sites as well.

## Architectural Decisions

1. **Reuse `enapter.http.api.AuthorizedRole`.**
   Both devices and sites share the same role enum.

2. **Add only `authorized_role`.**
   The Site response also contains `archived`, but that is out of scope for this change.

3. **No behavior change for `Device`.**
   Device handling of `authorized_role` remains unchanged.

## Requirements

1. `enapter.http.api.sites.Site` must expose `authorized_role: AuthorizedRole`.
2. `Site.from_dto()` must parse `authorized_role` from the API response DTO.
3. `Site.to_dto()` must serialize `authorized_role` using its enum value.
4. Unit tests must cover:
   - `Site.from_dto()` parses `authorized_role` correctly.
   - `Site.to_dto()` round-trips `authorized_role` correctly.
   - Existing site tests continue to work when `authorized_role` is present in mock responses.

## Constraints

- Do **not** add the `archived` field to `Site`.
- Do **not** modify `AuthorizedRole`.
- Do **not** change the existing `Device` field set or semantics.

## Acceptance Criteria

- `pytest tests/unit/test_http/test_api/test_sites` passes and includes assertions for `authorized_role`.
- `pytest tests/unit/test_http/test_api/test_devices` continues to pass.
- `pytest tests/unit/test_http/test_api/test_client` continues to pass.
- All existing tests continue to pass.
