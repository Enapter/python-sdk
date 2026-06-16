# SPEC-004: Rename `AuthorizedRole` to `AccessRole`

## Context

`enapter.http.api.AuthorizedRole` (introduced by SPEC-002 and reused for sites by SPEC-003) currently models the six-tier access concept returned by the HTTP API on `Device` and `Site` resources as the `authorized_role` field. The name `AuthorizedRole` mirrors that JSON field 1:1, but the underlying domain concept is broader: the Enapter [blueprint manifest schema](https://v3.developers.enapter.com/reference/blueprint/manifest/) defines the same six tiers as the `access_level` field on `properties`, `telemetry`, `commands`, and `configuration` (the docs even call them "access levels" in prose: "Defines the access level required to read the property value"). The HTTP-side name `authorized_role` is a leaky abstraction — it describes the value as "the role you were authorized as," when in fact both surfaces model "what access tier you have on this resource" and the manifest side uses the more accurate name.

The SDK does not yet parse manifest `access_level`, but the standalone framework in this repo works with blueprints and a shared type for both surfaces is the natural shape. Naming the enum after the manifest's `access_level` keeps the shared type aligned with the more accurate domain name. Without this rename, the day the SDK starts parsing manifest `access_level` we will either need a second enum or a confusingly-mixed one — both worse than renaming now while only one surface is in play.

The rename is intentionally narrow: only the type symbol changes. The attribute name on `Device` and `Site` stays `authorized_role`, and the JSON DTO key stays `authorized_role`, because both are server contracts and renaming them would be a much larger breaking change with no domain benefit.

## Architectural Decisions

1. **Rename the enum from `AuthorizedRole` to `AccessRole`.**
   The new name matches the manifest schema's `access_level` and reflects the actual domain concept (an access tier, not an authorization event).

2. **Keep the module path `enapter.http.api.authorization` unchanged.**
   The module is already the correct home for this concept; only the class name is wrong.

3. **Keep all enum members and string values unchanged.**
   Members remain `READONLY`, `USER`, `OWNER`, `INSTALLER`, `SYSTEM`, `VENDOR` with uppercase string values. These are dictated by the HTTP API.

4. **Keep the attribute name `authorized_role` on `Device` and `Site` unchanged.**
   The attribute is named after the JSON field. Renaming it would be a separate, larger decision that affects DTO mapping code and is out of scope for this spec.

5. **Keep the JSON DTO key `authorized_role` unchanged.**
   This is the server's contract. We map between the wire name and the type, not the other way around.

6. **Adopt an explicit case policy for future manifest use.**
   The enum stores uppercase string values to match the HTTP wire format. The blueprint manifest uses lowercase values for the same tiers. When manifest parsing is added in the future, callers construct the enum as `AccessRole(raw.upper())`. This is a parsing-convention decision, not a documentation requirement.

7. **No backward-compatibility alias for `AuthorizedRole`.**
   This is a breaking change. Consistent with the stance taken in SPEC-001 and SPEC-002. The SDK is pre-1.0 and the README explicitly warns that the API may change. Adding a deprecated alias would create a longer deprecation tail and ongoing maintenance burden with no compensating benefit.

## Requirements

1. Rename the class in `src/enapter/http/api/authorization.py` from `AuthorizedRole` to `AccessRole`. Add a brief docstring matching the style of other enums in the package (e.g., `engine_state.py`, `rule_state.py`, `runtime_version.py` — one line, descriptive, no inline-code references, no forward-looking speculation).

2. Update `src/enapter/http/api/__init__.py`:
   - Change the import to reference the new class name.
   - Update `__all__` to export `AccessRole` in the same position.

3. Update `src/enapter/http/api/devices/device.py` to reference `AccessRole` everywhere `AuthorizedRole` currently appears (the field annotation and the `from_dto` call). The attribute name `authorized_role` and the JSON key `authorized_role` stay as-is.

4. Update `src/enapter/http/api/sites/site.py` to reference `AccessRole` everywhere `AuthorizedRole` currently appears (the field annotation and the `from_dto` call). The attribute name `authorized_role` and the JSON key `authorized_role` stay as-is.

5. Update `tests/unit/test_http/test_api/test_authorization.py`:
   - Rename the test class to `TestAccessRole`.
   - Update the class docstring.
   - Update every reference from `AuthorizedRole` to `AccessRole`, including the parametrize values.

6. Update `tests/unit/test_http/test_api/test_devices/test_client.py` and `tests/unit/test_http/test_api/test_sites/test_client.py` (and any other test file that imports the old name) to reference `AccessRole`.

7. Verify there are no remaining references to the old name anywhere under `src/` or `tests/`. Historical references in `specs/SPEC-002-...md` and `specs/SPEC-003-...md` are allowed to remain as historical context.

## Constraints

- Do **not** change enum members, member order, or string values.
- Do **not** change the `authorized_role` attribute name on `Device` or `Site`.
- Do **not** change the `authorized_role` JSON DTO key in any `from_dto` / `to_dto` mapping.
- Do **not** add a backward-compatibility alias for `AuthorizedRole`.
- Do **not** change the module path `enapter.http.api.authorization`.
- Do **not** introduce manifest parsing in this change. The case policy decision is forward-looking; the work to parse blueprint `access_level` is a separate spec.

## Acceptance Criteria

- `enapter.http.api.AccessRole` is importable and exposes all six members with their existing uppercase string values.
- `enapter.http.api.AuthorizedRole` is no longer importable (a `from enapter.http.api import AuthorizedRole` raises `ImportError`).
- `Device.authorized_role: AccessRole` and `Site.authorized_role: AccessRole` type-check; the attribute name remains `authorized_role`.
- `Device.from_dto` and `Site.from_dto` still read the `authorized_role` key from the DTO; `to_dto` still writes the `authorized_role` key.
- The enum carries a brief docstring in the same style as other enums in the package.
- `pytest tests/unit/test_http/test_api/test_authorization.py` passes.
- `pytest tests/unit/test_http/test_api/test_devices` passes.
- `pytest tests/unit/test_http/test_api/test_sites` passes.
- `pytest tests/unit/test_http/test_api/test_client` passes.
- `make test` passes (full unit test suite).
- `make lint` passes.
- A codebase-wide search under `src/` and `tests/` for `AuthorizedRole` returns no matches.
