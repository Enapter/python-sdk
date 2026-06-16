# SPEC-001: Rename Authentication Code from `auth.py` to `authentication.py`

## Context

The `enapter.http.api` package currently contains `auth.py`, which holds the `Auth` class responsible for attaching the `X-Enapter-Auth-Token` and `X-Enapter-Auth-User` headers to outgoing requests. This is authentication logic, but the module and class names are ambiguous and collide conceptually with authorization.

`httpx` itself uses `Auth` as the base class for authentication *schemes*. Our concrete subclass should therefore have a more descriptive name, and the module should clearly indicate that it deals with authentication rather than authorization.

## Architectural Decisions

1. **Rename the module from `auth.py` to `authentication.py`.**
   This makes room for a future `authorization.py` module and removes ambiguity.

2. **Rename the class from `Auth` to `AuthenticationScheme`.**
   This follows the `httpx` terminology where subclasses of `Auth` are concrete authentication schemes.

3. **Rename the internal factory method from `_new_auth()` to `_new_authentication_scheme()`.**
   This keeps the client internals consistent with the new class name.

4. **No public API exposure.**
   `Auth` / `AuthenticationScheme` is not exported in `enapter.http.api.__all__`, so this change is internal to the SDK.

## Requirements

1. Rename `src/enapter/http/api/auth.py` to `src/enapter/http/api/authentication.py`.
2. Rename the `Auth` class inside that module to `AuthenticationScheme`.
3. Update `src/enapter/http/api/client.py`:
   - Import `AuthenticationScheme` from the new module path.
   - Rename the private method `_new_auth()` to `_new_authentication_scheme()`.
   - Update the method body to instantiate `AuthenticationScheme`.
4. Update any tests or test mocks that reference the old module path, class name, or method name.
5. Verify no other code references:
   - `enapter.http.api.auth`
   - class `Auth` from that module
   - `_new_auth`

## Constraints

- Do **not** change the authentication behavior (headers set, token/user handling, auth flow).
- Do **not** add new public exports.
- Do **not** keep backward-compatible aliases for the old names.

## Acceptance Criteria

- `pytest tests/unit/test_http/test_api/test_client.py` passes.
- A codebase-wide search for `enapter.http.api.auth`, `class Auth`, and `_new_auth` returns no references.
- All existing tests continue to pass.
