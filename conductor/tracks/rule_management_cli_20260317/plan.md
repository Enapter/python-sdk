# Implementation Plan: Rule Management CLI

## Phase 1: CLI Infrastructure and Registration [checkpoint: 5de1d89]

- [x] Task: Create `RuleCommand` group and register it
    - [x] Create `src/enapter/cli/http/api/rule_command.py`
    - [x] Register `RuleCommand` in `src/enapter/cli/http/api/rule_engine_command.py`
    - [x] Implement registration of sub-commands (placeholders for now)
- [x] Task: Conductor - User Manual Verification 'Phase 1: CLI Infrastructure and Registration' (Protocol in workflow.md)

## Phase 2: Read Operations (List and Get)

- [x] Task: Implement `rule list` command
    - [x] Create `src/enapter/cli/http/api/rule_list_command.py`
    - [x] Implement command logic and JSON output
- [x] Task: Implement `rule get` command
    - [x] Create `src/enapter/cli/http/api/rule_get_command.py`
    - [x] Implement command logic and JSON output
- [x] Task: Conductor - User Manual Verification 'Phase 2: Read Operations (List and Get)' (Protocol in workflow.md)

## Phase 3: Create and Delete Operations

- [x] Task: Implement `rule create` command
    - [x] Create `src/enapter/cli/http/api/rule_create_command.py`
    - [x] Implement command logic (handle `--script-file`, `--runtime-version`, `--exec-interval`, `--disable`)
- [x] Task: Implement `rule delete` command
    - [x] Create `src/enapter/cli/http/api/rule_delete_command.py`
    - [x] Implement command logic
- [x] Task: Conductor - User Manual Verification 'Phase 3: Create and Delete Operations' (Protocol in workflow.md)

## Phase 4: Update and State Management Operations

- [x] Task: Implement `rule update` (slug) command
    - [x] Create `src/enapter/cli/http/api/rule_update_command.py`
    - [x] Implement command logic
- [x] Task: Implement `rule update-script` command
    - [x] Create `src/enapter/cli/http/api/rule_update_script_command.py`
    - [x] Implement command logic (handle `--script-file`, `--runtime-version`, `--exec-interval`)
- [x] Task: Implement `rule enable` and `rule disable` commands
    - [x] Create `src/enapter/cli/http/api/rule_enable_command.py` and `src/enapter/cli/http/api/rule_disable_command.py`
    - [x] Implement command logic
- [x] Task: Conductor - User Manual Verification 'Phase 4: Update and State Management Operations' (Protocol in workflow.md)

## Phase 5: Finalization and Quality Check

- [x] Task: Final code quality check (linting)
- [x] Task: Verify overall CLI consistency and help messages
- [x] Task: Conductor - User Manual Verification 'Phase 5: Finalization and Quality Check' (Protocol in workflow.md)
