# Implementation Plan: Rule Management

This plan outlines the implementation of Rule management (create, list, get, update, enable/disable, delete) in the Enapter HTTP API Rule Engine client.

## Phase 1: Models and Foundation [checkpoint: c888a5d]

- [x] Task: Define `Rule`, `RuleScript`, and `RuntimeVersion`, and `RuleState` data models
    - [x] Create `src/enapter/http/api/rule_engine/rule.py`, `src/enapter/http/api/rule_engine/rule_script.py`, `src/enapter/http/api/rule_engine/runtime_version.py`, and `src/enapter/http/api/rule_engine/rule_state.py`
    - [x] Implement `Rule` and `RuleScript` dataclasses and `RuntimeVersion` and `RuleState` enums
    - [x] Implement `from_dto` and `to_dto` methods for all models
    - [x] Add unit tests for models in `tests/unit/test_http/test_api/test_rule_engine/test_rule.py`
- [x] Task: Export models in `src/enapter/http/api/rule_engine/__init__.py`
- [x] Task: Conductor - User Manual Verification 'Phase 1: Models and Foundation' (Protocol in workflow.md)

## Phase 2: Rule Management Implementation (Read Operations)

- [x] Task: Implement `List Rules` method
    - [x] Add `list_rules` method to `src/enapter/http/api/rule_engine/client.py`
    - [x] Write failing tests in `tests/unit/test_http/test_api/test_rule_engine/test_client.py`
    - [x] Implement method to pass tests
- [x] Task: Implement `Get Rule` method
    - [x] Add `get_rule` method to `src/enapter/http/api/rule_engine/client.py`
    - [x] Write failing tests
    - [x] Implement method to pass tests
- [~] Task: Conductor - User Manual Verification 'Phase 2: Rule Management Implementation (Read Operations)' (Protocol in workflow.md)

## Phase 3: Rule Management Implementation (Write Operations)

- [ ] Task: Implement `Create Rule` method
    - [ ] Add `create` method to `src/enapter/http/api/rule_engine/client.py`
    - [ ] Write failing tests (including base64 encoding check)
    - [ ] Implement method to pass tests
- [ ] Task: Implement `Update Rule` (slug) method
    - [ ] Add `update` method to `src/enapter/http/api/rule_engine/client.py`
    - [ ] Write failing tests
    - [ ] Implement method to pass tests
- [ ] Task: Implement `Update Rule Script` method
    - [ ] Add `update_script` method to `src/enapter/http/api/rule_engine/client.py`
    - [ ] Write failing tests
    - [ ] Implement method to pass tests
- [ ] Task: Implement `Delete Rule` method
    - [ ] Add `delete` method to `src/enapter/http/api/rule_engine/client.py`
    - [ ] Write failing tests
    - [ ] Implement method to pass tests
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Rule Management Implementation (Write Operations)' (Protocol in workflow.md)

## Phase 4: Rule State Management

- [ ] Task: Implement `Enable Rule` and `Disable Rule` methods
    - [ ] Add `enable` and `disable` methods to `src/enapter/http/api/rule_engine/client.py`
    - [ ] Write failing tests
    - [ ] Implement methods to pass tests
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Rule State Management' (Protocol in workflow.md)

## Phase 5: Integration and Finalization

- [ ] Task: Add integration tests for all new Rule management methods
    - [ ] Create `tests/integration/test_rule_engine_management.py` (or similar)
    - [ ] Verify full flows against a mock or real environment if possible
- [ ] Task: Final code quality check (linting, coverage)
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Integration and Finalization' (Protocol in workflow.md)
