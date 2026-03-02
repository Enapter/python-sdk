# Track Specification: Add basic unit-tests for the HTTP client.

## Objective
Implement basic unit testing coverage for the HTTP client module within the Enapter Python SDK. This ensures reliability and stability of the client's core operations like connecting to the Enapter API, managing sites, and handling telemetry.

## Scope
- Focus on `src/enapter/http/api/client.py` and its related dependencies.
- Use `pytest` for running and structuring the tests.
- Use `httpx` mocking features (like `pytest-httpx` or similar) if needed, or stick to basic unit-tests on the existing public methods.

## Exclusions
- Integration tests that require live Enapter Cloud credentials.
- Tests for MQTT client or Standalone devices.