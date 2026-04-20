## [0.17.2] - 2026-04-15

### 🚀 Features

- *(http-api)* Support fetching raised alerts for devices
- *(cli)* Add support for expanding raised alert names in device commands

### ⚙️ Miscellaneous Tasks

- Drop conductor
- Bump version to 0.17.2
## [0.17.1] - 2026-04-07

### 🚀 Features

- *(http-api)* Add CHILD device type

### 🐛 Bug Fixes

- *(security)* Replace insecure random with secrets for hardware ID

### 🧪 Testing

- Add error test for `parse_command_arguments`
- Refine error test for `parse_command_arguments`
- Refactor imports in `command_arguments` tests
- Add comprehensive tests for `async_.generator`
- Add tests for `DataType.parse_value`
- Add test for `check_error` (#42)
- Add unit tests for HTTP API blueprints (#44)
- Add unit tests for Labels string parsing (#45)
- Add tests for `parse_site_location` edge cases (#38)

### ⚙️ Miscellaneous Tasks

- Merge pull request #36 from Enapter/add-error-test-for-parse-command-arguments
- Merge pull request #37 from Enapter/test-generator-coverage
- Merge pull request #43 from Enapter/security-fix-hardware-id-randomness
- Merge pull request #40 from Enapter/testing-improvement-data-type-parse-value
- Bump version to 0.17.1
## [0.17.0] - 2026-03-17

### 🚀 Features

- *(http-api)* Create Engine data model for rule engine management
- *(http-api)* Implement RuleEngine client
- *(http-api)* Integrate RuleEngine client into main Client
- *(http-api)* Use EngineState enum for rule engine
- *(cli)* Implement Rule Engine management commands
- *(cli)* Make `-o` optional for blueprint download
- *(http-api/rule_engine)* Checkpoint Phase 1
- *(http-api/rule_engine)* Checkpoint Phase 2
- *(http-api/rule_engine)* Checkpoint Phase 3
- *(http-api/rule_engine)* Checkpoint Phase 4
- *(http-api/rule_engine)* Add `exec_interval` to `RuleScript` for V1 support
- *(cli)* Checkpoint Phase 1
- *(cli)* Implement rule management
- *(http-api)* Make `list_rules` an async generator

### 🐛 Bug Fixes

- *(conductor)* Apply review suggestions for HTTP client tests
- *(http-api)* Update Engine data model to match reference
- *(http-api)* Use `engine` key for rule engine response parsing

### 📚 Documentation

- *(http-api)* Update Rule Engine management example
- *(http-api)* Update Rule Engine example for EngineState enum
- *(http-api)* Add docstrings to Rule Engine module and tests
- *(http-api)* Remove rule engine management example
- *(conductor)* Synchronize rule engine documentation
- *(conductor)* Simplify workflow requirements
- *(conductor)* Switch to per-phase commits
- *(conductor)* Adapt development commands to Python environment

### 🎨 Styling

- *(test)* Follow import style guide in rule engine tests

### 🧪 Testing

- *(http)* Add unit tests for client initialization and transport
- *(http)* Add unit tests for Sites API client
- *(http-api)* Add missing __init__.py for test_rule_engine

### ⚙️ Miscellaneous Tasks

- *(conductor)* Add setup files
- *(conductor)* Mark client test task complete
- *(conductor)* Checkpoint Phase 1
- *(conductor)* Mark Phase 1 initialization tests complete
- *(conductor)* Mark sites test task complete
- *(conductor)* Checkpoint Phase 2
- *(conductor)* Mark Phase 2 sites tests complete
- *(conductor)* Finalize track specification and formatting
- *(conductor)* Mark HTTP client unit tests complete
- *(conductor)* Mark review suggestions complete
- *(conductor)* Mark HTTP client unit tests complete
- *(conductor)* Add rule engine management track
- *(conductor)* Mark engine data model complete
- *(conductor)* Mark RuleEngine client complete
- *(conductor)* Mark RuleEngine integration complete
- *(conductor)* Mark RuleEngine tests complete
- *(conductor)* Verify Phase 1
- *(conductor)* Checkpoint Phase 1: HTTP API Client
- *(conductor)* Complete Phase 1
- *(conductor)* Verify Phase 2
- *(conductor)* Checkpoint Phase 2: CLI Implementation
- *(conductor)* Complete rule engine track
- *(conductor)* Complete Phase 1
- *(conductor)* Complete Phase 2
- *(conductor)* Complete Phase 3
- *(conductor)* Complete Phase 4
- *(conductor)* Complete Phase 5
- *(conductor)* Complete rule engine track
- *(conductor)* Archive rule engine track
- *(conductor)* Archive HTTP client track
- *(conductor)* Drop HTTP client track from registry
- *(conductor)* Cleanup track folders
- *(conductor)* Initialize Rule Management CLI track
- *(conductor)* Add rule management cli track
- *(conductor)* Complete Phase 1
- *(conductor)* Complete rule management track
- *(conductor)* Mark rule management track complete
- *(conductor)* Archive rule management track
- Merge pull request #35 from Enapter/rnovatorov/http-api-rule-management
- Bump version to 0.17.0

### ◀️ Revert

- Temporarily disable integration tests on CI
## [0.16.0] - 2026-03-02

### 🚀 Features

- *(http-api)* Add HTTP time sync protocol
- *(mqtt)* Upgrade aiomqtt to 2.5 and fix types

### 💼 Other

- Bump version, commit, and tag

### 🚜 Refactor

- *(http-api)* Revert to property-based subclient access

### ⚙️ Miscellaneous Tasks

- Bump version to 0.16.0
## [0.15.1] - 2026-02-10

### 🚀 Features

- *(http-api)* Support username-based authentication

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.15.0] - 2026-02-10

### 🚀 Features

- *(http-api)* Use `httpx.Auth` for authentication
- *(http-api)* Allow per-service authentication override

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.14.4] - 2026-01-30

### 🐛 Bug Fixes

- *(http-api/sites)* Allow optional location lat/lon
- *(http-api/commands)* Add missing execution state enum value

### ⚙️ Miscellaneous Tasks

- Bump version
- Temporarily disable integration tests
## [0.14.3] - 2026-01-20

### 🐛 Bug Fixes

- *(http-api/telemetry)* Correct timestamp parsing in latest datapoint

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.14.2] - 2026-01-20

### 🚀 Features

- *(http-api/telemetry)* Support string array data type

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.14.1] - 2026-01-20

### 🐛 Bug Fixes

- *(http-api/sites)* Correct site version literal
- *(http-api)* Ensure response content is read in `check_error`

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.14.0] - 2026-01-19

### 🚀 Features

- *(http-api/devices)* Add optional site ID filtering
- *(http-api)* Support latest telemetry retrieval
- *(http-api/telemetry)* Implement timeseries retrieval

### 🐛 Bug Fixes

- Correct links to examples
- *(http-api/devices)* Use prettier random names
- *(examples/standalone)* Remove unnecessary brackets in snmp-eaton-ups

### 💼 Other

- Extract regex to variable in Makefile
- Fix `DOCKER_IMAGE_TAG` usage in Makefile
- Print diff for black lint failure

### ⚙️ Miscellaneous Tasks

- Handle KeyboardInterrupt in main
- Add `mcp_servers.json` to .gitignore
- Build and push Docker image
- Bump version

### ◀️ Revert

- Add `mcp_servers.json` to .gitignore
## [0.13.1] - 2026-01-06

### 🚀 Features

- *(http-api)* Implement Sites API client with CRUD operations
- *(examples/http)* Add site listing example using Sites API
- *(http-api/sites)* Support `/v3/site` shortcut
- *(http-api/sites)* Extend `update` parameters
- *(cli/http-api)* Add `site` command
- *(http-api)* Support expanding device manifest
- *(http-api)* Replace `get device manifest` with expansion
- *(http-api)* Support expanding device properties
- *(http-api)* Support expanding device connectivity
- *(http-api)* Support expanding device communication info
- *(http-api)* Add expansion support to device listing
- *(cli/http-api)* Simplify subcommand names
- *(http-api)* Implement basic blueprint support
- *(http-api)* Implement device commands
- *(http-api/blueprints)* Implement validation
- *(http-api/blueprints)* Implement retrieval
- *(http-api/devices)* Add VUCM and Lua device creation
- *(http-api/devices)* Add `slug` to standalone provisioning requests
- *(http-api/devices)* Auto-generate device name if omitted
- *(examples/http)* Support JSON output
- *(examples/mqtt)* Add RL6 implementation using API

### 🐛 Bug Fixes

- *(cli/http-api)* Correct `name` argument description for standalone device creation
- *(http-api/sites)* Correct Site model
- *(standalone/mqtt)* Handle publish command response errors in adapter

### 📚 Documentation

- *(examples/standalone)* Prioritize communication config in README

### ⚙️ Miscellaneous Tasks

- Initial project plan
- Merge pull request #29 from Enapter/copilot/implement-sites-api-client
- Merge pull request #30 from Enapter/rnovatorov/http
- Merge pull request #31 from Enapter/rnovatorov/http
- Bump version
## [0.13.0] - 2025-11-20

### 🚀 Features

- *(http-api)* Implement error message parsing
- *(http-api)* Support allowing HTTP
- *(http-api/devices)* Add missing device types
- Add basic CLI for HTTP API
- *(http-api/devices)* Add standalone device creation
- *(http-api/devices)* Add device listing
- *(http-api/devices)* Add device deletion
- *(http-api/devices)* Add device updates
- *(http-api/devices)* Support blueprint assignment
- *(http-api/devices)* Support fetching device manifest

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.12.2] - 2025-11-19

### 💼 Other

- Include README in bump-version file list
- Rename test targets in Makefile

### 🚜 Refactor

- *(test)* Align unit tests with package structure

### 📚 Documentation

- Update version in README
- Fix grammatical error in README

### 🧪 Testing

- *(mqtt/api)* Add more unit tests
- *(standalone)* Add unit tests
- Remove fake data generator from tests
- Run tests

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.12.1] - 2025-11-12

### ⚙️ Miscellaneous Tasks

- Set `upload_to_pypi` dependency on `run_checks`
- Bump version to 0.12.1 for PyPI upload
## [0.12.0] - 2025-11-12

### 🚀 Features

- *(examples/mqtt)* Add RL6 simulator
- *(mqtt)* Export `Message`
- *(mqtt/api)* Add `LOG` to `CommandState`
- Add `standalone` package
- Add basic HTTP API support
- *(standalone)* Allow `cmd_prefix` configuration in device
- *(mqtt)* Suppress logging on publisher disconnection
- *(standalone/vucm)* Use different intervals for properties and telemetry
- *(standalone)* Allow overriding MQTT host in communication config
- *(standalone)* Support `ENAPTER_VUCM_BLOB` with deprecation warning
- *(examples/http)* Add `get_device_by_id`
- *(async)* Restore `async_.Routine` and support optional task group

### 🐛 Bug Fixes

- *(mqtt)* Handle cancellation during client connection
- *(http-api)* Correct time sync protocol parsing in devices
- *(examples/standalone)* Correct psutil-battery example
- *(examples/standalone)* Correct RL6 simulator example
- *(examples/standalone)* Correct wttr-in example
- *(examples/standalone)* Correct smart fan example
- *(standalone)* Propagate `CancelledError` in app
- *(examples/standalone)* Attempt fix for snmp-eaton-ups
- *(examples/standalone)* Attempt fix for zigbee2mqtt
- *(examples/mqtt)* Correct pub/sub example
- *(examples/standalone)* Correct wttr-in alerts and configuration environment variable

### 💼 Other

- Use `src` directory for package layout
- Add `httpx` to dependencies
- Drop support for Python versions below 3.11
- Add `py.typed` marker file

### 🚜 Refactor

- *(mqtt)* Move `DeviceChannel` from `api` to `mqtt`
- *(mqtt)* Define API more explicitly
- *(mqtt)* Move `DeviceChannel` back to `api`
- *(mqtt/api)* Define one class per file
- *(standalone)* Use ABC for device to enable convenient logging
- *(async)* Use `asyncio.TaskGroup` instead of `async_.Routine`
- *(config)* Normalize environment variable handling
- *(standalone)* Update configuration for API v3 support
- *(examples)* Rename `vucm` to `standalone`
- *(standalone)* Split device protocol and base class
- *(standalone)* Wrap command results in objects
- *(standalone)* Accept `DeviceProtocol` instead of `Device` in `run`
- *(standalone)* Make `Device.logger` property synchronous
- Split MQTT client and MQTT API
- *(standalone)* Rename `DeviceDriver` to `MQTTAdapter`
- *(mqtt/standalone)* Move logging from device channel to MQTT adapter

### 📚 Documentation

- Update README with recent changes
- Refine READMEs

### 🎨 Styling

- *(examples/mqtt)* Format pub/sub code
- Set black profile for isort
- Modernize type annotations
- *(setup)* Add type annotations
- *(test)* Add type annotations to tests

### 🧪 Testing

- *(mqtt)* Fix missing alerts null field in unit tests
- Add mypy check for setup and tests
- Add unit tests for `async_.Routine`
- Fix `Generator` type annotations in tests

### ⚙️ Miscellaneous Tasks

- Remove `types` module
- Drop `vucm` package and tests
- *(examples/mqtt)* Remove RL6 simulator
- Bump version to 0.12.0
- Merge pull request #21 from Enapter/rnovatorov/dev
- Restore routine
- Make publishing dependent on check success
- Fix job names
## [0.11.4] - 2025-09-30

### 🚀 Features

- *(examples/mqtt)* Handle publish errors in pub/sub

### 🚜 Refactor

- *(mqtt)* Export `Error`

### 📚 Documentation

- Fix pip install command formatting in README

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.11.3] - 2025-09-30

### 🚀 Features

- Reapply update to aiomqtt 2.4
- Add missing type annotations
- *(examples/mqtt)* Add pub/sub example

### 💼 Other

- Update aiomqtt to 2.4
- Upgrade json-log-formatter to 1.1
- Upgrade dnspython to 2.8
- Add mypy to dev dependencies in Pipfile
- Add mypy lint target to Makefile

### 🚜 Refactor

- *(examples/vucm)* Remove redundant dot fields from RL6-sim manifest
- *(log)* Remove `taskName` from JSON formatter `extra` fields

### 📚 Documentation

- Recommend pinning version in installation instructions

### 🎨 Styling

- *(mqtt)* Fix import ordering in client

### ⚙️ Miscellaneous Tasks

- Bump version
- Bump version
- Trigger workflow only on push
- Merge pull request #20 from Enapter/rnovatorov/dev
- *(examples)* Bump version

### ◀️ Revert

- Update aiomqtt to 2.4
## [0.10.2] - 2025-09-25

### 🐛 Bug Fixes

- *(vucm)* Correct command execution in device

### 🚜 Refactor

- *(vucm)* Clean up device initialization

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.10.1] - 2025-07-31

### 🐛 Bug Fixes

- *(log)* Avoid using `datetime.UTC` alias in JSON formatter

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.10.0] - 2025-07-28

### 🚀 Features

- *(vucm)* Add `config_prefix` keyword argument to `run`

### 🐛 Bug Fixes

- *(log)* Correct timezone usage in JSON formatter

### 💼 Other

- Drop support for Python 3.8
- Explicitly install setuptools in Pipfile

### 🚜 Refactor

- *(vucm)* Explicitly mark tasks and commands
- *(types)* Add recursive JSON definition

### 📚 Documentation

- Update task and command descriptions in README

### 🧪 Testing

- Fix fields check in logging unit tests

### ⚙️ Miscellaneous Tasks

- Bump version
- Use Python 3.11 for PyPI publishing
## [0.9.2] - 2024-04-16

### 🚀 Features

- *(examples)* Add Zigbee2Mqtt integration

### 💼 Other

- Upgrade dnspython

### ⚙️ Miscellaneous Tasks

- Merge pull request #16 from Enapter/zigbee2mqtt_example
- Bump version
- Merge pull request #18 from Enapter/rnovatorov/upgrade-dnspython
## [0.9.1] - 2023-11-14

### 🐛 Bug Fixes

- *(vucm)* Correct device channel instantiation

### 💼 Other

- Add bump-version target to Makefile

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.9.0] - 2023-11-14

### 🚀 Features

- *(examples)* Add standalone VUCM for Eaton UPS monitoring over SNMP
- *(examples/vucm)* Use `Device.run_in_thread`
- *(examples/vucm)* Add human-readable battery statuses for Eaton UPS

### 🐛 Bug Fixes

- *(examples/vucm)* Satisfy linters in snmp-eaton-ups

### 🚜 Refactor

- *(examples/vucm)* Rename README in snmp-eaton-ups
- *(examples/vucm)* Use object for env vars in snmp-eaton-ups docker-compose
- *(examples/vucm)* Pythonize script in snmp-eaton-ups
- Remove two-level relative imports
- *(mqtt)* Extract API into separate package
- *(mqtt)* Rename `DeviceLogSeverity` to `LogSeverity`

### 🎨 Styling

- *(examples/vucm)* Run prettier on snmp-eaton-ups README

### 🧪 Testing

- *(mqtt)* Rename `TestMQTT` to `TestClient` in integration tests

### ⚙️ Miscellaneous Tasks

- Merge pull request #13 from Enapter/nvk/snmp-vucm-example
- Merge pull request #15 from Enapter/nvk/snmp-eaton-ups-improvement
- Bump version
- Merge pull request #17 from Enapter/rnovatorov/dev
- Pin Python version for publishing
## [0.8.0] - 2023-07-25

### 🚜 Refactor

- *(async)* Replace `run_in_executor` with `Device.run_in_thread`

### ⚙️ Miscellaneous Tasks

- Test on Python 3.11 instead of 3.7
- Bump version
- Merge pull request #14 from Enapter/rnovatorov/dev
## [0.7.3] - 2023-07-21

### 🚀 Features

- *(async)* Add `run_in_executor` helper

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.7.2] - 2023-07-18

### 💼 Other

- Replace asyncio-mqtt with aiomqtt in setup

### ⚙️ Miscellaneous Tasks

- *(examples)* Upgrade Enapter version
- Bump version
- Merge pull request #12 from Enapter/rnovatorov/dev
## [0.7.1] - 2023-06-15

### 💼 Other

- Upgrade asyncio-mqtt

### 🎨 Styling

- Reformat code with latest black

### ⚙️ Miscellaneous Tasks

- *(examples/vucm)* Upgrade SDK version in requirements
- Merge pull request #11 from Enapter/rnovatorov/upgrade-asyncio-mqtt
- Bump version
## [0.7.0] - 2023-01-17

### 🚀 Features

- *(mqtt)* Implement unsubscribe

### 🐛 Bug Fixes

- *(mqtt)* Fix reconnect logic

### 💼 Other

- Upgrade asyncio-mqtt

### 🚜 Refactor

- Split unit tests into separate package
- *(mqtt)* Remove unnecessary mutex

### 🧪 Testing

- Add integration tests

### ⚙️ Miscellaneous Tasks

- *(examples/vucm)* Upgrade SDK version in requirements
- Merge pull request #9 from Enapter/rnovatorov/integration-tests
- Merge pull request #10 from Enapter/rnovatorov/upgrade-asyncio-mqtt
- Bump version
## [0.6.6] - 2023-01-04

### 🚀 Features

- *(mqtt)* Unreserve timestamp field
- *(examples/vucm)* Add psutil-battery example

### 💼 Other

- Add dev dependencies update target to Makefile
- Add faker as test dependency

### 📚 Documentation

- Update host networking information in README

### 🧪 Testing

- Add fake data generator
- Verify timestamp field reservation

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.6.5] - 2022-10-27

### 🚀 Features

- *(examples/vucm)* Support both macOS and Linux

### 💼 Other

- Remove aiohttp from dependencies

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.6.4] - 2022-10-27

### 🐛 Bug Fixes

- *(mqtt)* Prevent infinite loop in mDNS resolution

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.6.3] - 2022-10-27

### 🚀 Features

- *(mdns)* Resolve via DNS first for macOS Docker compatibility

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.6.2] - 2022-10-26

### 🚀 Features

- *(mqtt)* Avoid duplicate logging of host and port
- *(mqtt)* Log hostname when mDNS resolution fails

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.6.1] - 2022-10-26

### 🐛 Bug Fixes

- *(examples/vucm)* Execute docker_run from example directory

### 🚜 Refactor

- *(mdns)* Configure DNS resolver

### ⚙️ Miscellaneous Tasks

- *(examples/vucm)* Bump SDK version
- *(examples/vucm)* Disable quiet docker image build
- Bump version
## [0.6.0] - 2022-10-25

### 🚀 Features

- *(mqtt)* Retry mDNS resolution
- *(mqtt)* Expose hardware and channel IDs as device channel properties
- *(examples/vucm)* Catch and log more exceptions in wttr-in

### 🚜 Refactor

- *(vucm)* Tee logs to standard library logger
- *(vucm)* Log failed task using logger

### 📚 Documentation

- Update README

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.5.0] - 2022-10-18

### 🚀 Features

- *(async/generator)* Support Python 3.7

### 💼 Other

- Add json-log-formatter as dependency

### 🚜 Refactor

- *(async)* Remove unused `block`
- *(log)* Improve logging for 3rd-party application compatibility

### 🧪 Testing

- Increase pytest verbosity in Makefile

### ⚙️ Miscellaneous Tasks

- *(examples/vucm)* Upgrade SDK version in requirements
- Merge pull request #8 from Enapter/rnovatorov/rework-logging
- Bump version
## [0.4.0] - 2022-10-17

### 🚀 Features

- Add install script for Avahi daemon
- *(mdns)* Add mDNS resolver and bump version to 0.4.0
- *(mqtt)* Support mDNS hostname resolution

### 🐛 Bug Fixes

- *(examples/rl6-simulator)* Use proper channel ID in docker_run.sh

### 💼 Other

- Add dnspython as dependency
- Specify long description content type in setup

### 📚 Documentation

- Add 'Writing your own UCM' instructions
- Update README
- *(vucm)* Add note about gateway and host network

### ⚙️ Miscellaneous Tasks

- *(examples)* Send properties in wttr-in
- Merge pull request #3 from Enapter/abakin/docs
- Merge pull request #4 from Enapter/abakin/avahi-ext
- *(examples/wttr-in)* Bump requirements
- *(examples)* Migrate to Debian-based images and use Avahi install script
- Remove extensions
- Bump version
- Merge pull request #7 from Enapter/rnovatorov/mdns-resolve
## [0.3.0] - 2022-09-26

### 🚀 Features

- Allow overriding channel ID
- *(examples)* Add RL6 simulator

### 🐛 Bug Fixes

- Copy dictionary before modification in telemetry/properties

### ⚙️ Miscellaneous Tasks

- Merge pull request #1 from Enapter/abakin/rl6-vucm
## [0.2.1] - 2022-09-21

### 🚀 Features

- *(examples)* Add requirements.txt for zhimi-fan-za5
- *(examples)* Add wttr-in VUCM
- *(examples)* Add docker run script for zhimi-fan-za5
- *(examples)* Add docker run script for wttr-in

### 🚜 Refactor

- *(examples)* Remove redundant device factory in wttr-in

### 📚 Documentation

- Add PyPI badge to README

### ⚙️ Miscellaneous Tasks

- *(vucm)* Make start optional
- Bump version
## [0.2.0] - 2022-09-21

### 🚀 Features

- *(examples)* Add VUCM usage docstrings
- *(mqtt)* Enumerate device log severity
- *(vucm)* Improve public API
- *(examples)* Add zhimi-fan-za5 VUCM
- *(examples)* Return command results in zhimi-fan-za5
- *(examples)* Simplify operation mode check in zhimi-fan-za5

### 🚜 Refactor

- *(log)* Make `new` idempotent

### 📚 Documentation

- Add CI and code style badges to README
- Add WIP banner to README
- Make WIP banner bold in README

### ⚙️ Miscellaneous Tasks

- Bump version
## [0.1.0] - 2022-09-19

### 🚀 Features

- Add .gitignore
- Add library code
- Add setup script
- Add Pipfile
- *(examples)* Add initial VUCM example device
- *(mqtt)* Remove sleep after cancelled connect

### 🐛 Bug Fixes

- *(setup)* Correct project URL

### 💼 Other

- Move pipenv installation from CI to Makefile
- Add PyPI upload target
- Add isort configuration

### 📚 Documentation

- Add installation and usage instructions to README

### 🧪 Testing

- Specify explicit path for tests in Makefile
- Add tests for async routine

### ⚙️ Miscellaneous Tasks

- Configure linters and tests
- Configure CI
- *(vucm)* Load config from blob
- Add workflow to publish to PyPI
- Disable upload to test PyPI
