# Enapter Python SDK

[![CI](https://github.com/Enapter/python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/Enapter/python-sdk/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/enapter.svg)](https://pypi.org/project/enapter)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Enapter software development kit for Python.

:warning: **This project is work in progress. The API is not stable and may change at any time.** :warning:

## Installation

Stable from PyPI:

```bash
pip install enapter
```

Latest for GitHub:

```bash
pip install git+https://github.com/Enapter/python-sdk#egg=enapter
```

## Usage

Checkout [examples](examples).

## Writing your own UCM

### Sending telemetry and properties
You should define method with `task_` prefix to do periodic job. Typically telemetry sends every 1 seconds and properties every 10 seconds. So, the simplest way to implement this — define two task methods. Refer to wttr-in example for working sorce code.

### Handle commands
You should define method with name `cmd_<command_name_in_manfiest>` with defined arguments. The zhimi-fan-za5 example has a different types of command.

### Sending alerts
The alerts are stored in `self.alerts` set object. They should be updated before every `send_telemetry` call, because alerts are sending with telemetry.
