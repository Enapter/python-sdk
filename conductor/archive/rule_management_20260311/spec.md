# Specification: Rule Management

## Overview
This track implements comprehensive rule management within the Enapter HTTP API Rule Engine client. This includes creating, listing, retrieving, updating, enabling/disabling, and deleting rules via the Enapter Cloud HTTP API.

## Functional Requirements
The `enapter.http.api.rule_engine.Client` will be extended with methods to:
1.  **Create Rule**: `POST` a new rule with a `slug`, `script` (code and runtime version), and optional `disabled` flag.
2.  **List Rules**: `GET` all rules for a specific site or the default site.
3.  **Get Rule**: `GET` a specific rule by its ID.
4.  **Update Rule**: `PATCH` an existing rule's `slug`.
5.  **Update Rule Script**: `POST` a new `script` (code and runtime version) for an existing rule.
6.  **Enable Rule**: `POST` to enable a rule.
7.  **Disable Rule**: `POST` to disable a rule.
8.  **Delete Rule**: `DELETE` a rule by its ID.

## Data Model: Rule
A `Rule` model will be introduced in `src/enapter/http/api/rule_engine/rule.py`, including:
- `id`: Unique identifier for the rule.
- `slug`: Human-readable identifier.
- `disabled`: Boolean indicating if the rule is disabled.
- `state`: Execution state (e.g., `STARTED`, `STOPPED`).
- `script`: An object containing:
    - `code`: The rule's script code (base64 encoded string).
    - `runtime_version`: The runtime environment version (`V1` or `V3`).

## Technical Requirements
- **Integration**: Methods will be added to `enapter.http.api.rule_engine.Client`.
- **Async Strategy**: All API calls will be asynchronous using `httpx.AsyncClient`.
- **Error Handling**: Use the existing `enapter.http.api.check_error` mechanism which raises generic HTTP client exceptions for failed requests.
- **Base64 Encoding**: The client should handle base64 encoding/decoding of the rule script code for ease of use.
- **Modern Python**: Adhere to Python 3.11+ patterns and typing.

## Acceptance Criteria
- [ ] Users can create a rule by providing a slug and script code.
- [ ] Users can list all rules for a site.
- [ ] Users can retrieve a specific rule by ID.
- [ ] Users can update a rule's slug.
- [ ] Users can update a rule's script code and runtime version.
- [ ] Users can enable and disable a rule.
- [ ] Users can delete a rule.
- [ ] All new methods are fully tested with unit and integration tests.

## Out of Scope
- Management of Rule Engine itself (suspend/resume/get state) is already implemented and remains unchanged.
- Frontend/CLI integration for these new methods.
