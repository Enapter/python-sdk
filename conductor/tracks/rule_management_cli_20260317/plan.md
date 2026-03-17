# Implementation Plan: Rule Management CLI

## Phase 1: CLI Infrastructure and Registration [checkpoint: 5de1d89]

- [x] Task: Create `RuleCommand` group and register it
    - [x] Create `src/enapter/cli/http/api/rule_command.py`
    - [x] Register `RuleCommand` in `src/enapter/cli/http/api/rule_engine_command.py`
    - [x] Implement registration of sub-commands (placeholders for now)
- [x] Task: Conductor - User Manual Verification 'Phase 1: CLI Infrastructure and Registration' (Protocol in workflow.md)

## Phase 2: Read Operations (List and Get)

- [ ] Task: Implement `rule list` command
    - [ ] Create `src/enapter/cli/http/api/rule_list_command.py`
    - [ ] Implement command logic and JSON output
- [ ] Task: Implement `rule get` command
    - [ ] Create `src/enapter/cli/http/api/rule_get_command.py`
    - [ ] Implement command logic and JSON output
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Read Operations (List and Get)' (Protocol in workflow.md)

## Phase 3: Create and Delete Operations

- [ ] Task: Implement `rule create` command
    - [ ] Create `src/enapter/cli/http/api/rule_create_command.py`
    - [ ] Implement command logic (handle `--script-file`, `--runtime-version`, `--exec-interval`, `--disable`)
- [ ] Task: Implement `rule delete` command
    - [ ] Create `src/enapter/cli/http/api/rule_delete_command.py`
    - [ ] Implement command logic
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Create and Delete Operations' (Protocol in workflow.md)

## Phase 4: Update and State Management Operations

- [ ] Task: Implement `rule update` (slug) command
    - [ ] Create `src/enapter/cli/http/api/rule_update_command.py`
    - [ ] Implement command logic
- [ ] Task: Implement `rule update-script` command
    - [ ] Create `src/enapter/cli/http/api/rule_update_script_command.py`
    - [ ] Implement command logic (handle `--script-file`, `--runtime-version`, `--exec-interval`)
- [ ] Task: Implement `rule enable` and `rule disable` commands
    - [ ] Create `src/enapter/cli/http/api/rule_enable_command.py` and `src/enapter/cli/http/api/rule_disable_command.py`
    - [ ] Implement command logic
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Update and State Management Operations' (Protocol in workflow.md)

## Phase 5: Finalization and Quality Check

- [ ] Task: Final code quality check (linting)
- [ ] Task: Verify overall CLI consistency and help messages
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Finalization and Quality Check' (Protocol in workflow.md)
