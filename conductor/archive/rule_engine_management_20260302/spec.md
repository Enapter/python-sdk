# Specification: Rule Engine Management

## Overview
Implement support for managing the Enapter Rule Engine through the HTTP API client and CLI. This includes retrieving the current state, suspending, and resuming the rule engine for a specific site.

## Functional Requirements

### HTTP API Client
- Add a new `rule_engine` property to the main `Client` in `src/enapter/http/api/client.py`.
- Implement a new module `src/enapter/http/api/rule_engine/` containing:
  - `Engine` dataclass for representing the engine state.
  - `Client` class with the following asynchronous methods:
    - `get(site_id: str | None) -> Engine`: Retrieves the rule engine status.
    - `suspend(site_id: str | None) -> Engine`: Suspends the rule engine.
    - `resume(site_id: str | None) -> Engine`: Resumes the rule engine.
- If `site_id` is not provided, the client should use the default site endpoint (e.g., `v3/site/rule_engine`).

### CLI
- Add a new command group `enapter api rule-engine` with the following subcommands:
  - `get [--site-id SITE_ID]`: Display current rule engine status.
  - `suspend [--site-id SITE_ID]`: Suspend the rule engine.
  - `resume [--site-id SITE_ID]`: Resume the rule engine.

## Non-Functional Requirements
- **Consistency:** Follow existing patterns for HTTP API modules (dataclasses with `from_dto`, async `httpx` calls).
- **Error Handling:** Use `api.check_error` for all HTTP responses.
- **Testing:** Comprehensive unit tests for the **API client** methods. **CLI command unit tests are excluded from this track.**
- **Documentation:** Proper type hints and docstrings.

## Out of Scope
- Management of individual rules (Create, List, Update, Delete, Batch operations).
- Management of rule engine scripts.
- Telemetry related to rule engine execution.
