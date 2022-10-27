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

## Implementing your own VUCM

### Device Telemetry and Properties

Every method of `enapter.vucm.Device` subclass with a name that starts with
`task_` prefix is considered a _device task_. When such a device is started,
all of its tasks are started as well. Device tasks are started in random order
and are being executed concurrently in the background. If a device task returns
or raises an exception, device routine is terminated. A typical use of the task
is to run a periodic job to send device telemetry and properties.

In order to send telemetry and properties define two corresponding device
tasks. It is advised (but is not obligatory) to send telemetry every **1
second** and to send properties every **10 seconds**.

Examples:

- [wttr-in](examples/vucm/wttr-in)

### Device Commands

Every method of `enapter.vucm.Device` subclass with a name that starts with
`cmd_` prefix is considered a _device command handler_. Device command handlers
receive the same arguments as described in device Blueprint manifest and can
optionally return a payload as `dict`.

In order to handle device commands define corresponding device command
handlers.

Examples:

- [zhimi-fan-za5](examples/vucm/zhimi-fan-za5)

### Device Alerts

Device alerts are stored in `self.alerts`. It is a usual Python `set`, so you
can add an alert using `alerts.add`, remove an alert `alerts.remove` and clear
alerts using `alerts.clear`.

Alerts are sent only as part of telemetry, so in order to report device alert,
use `send_telemetry` with any payload.

## Running your own VUCM via Docker

A simple Dockerfile can be:

```
FROM python:3.10-alpine3.16

WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt requirements.txt
RUN .venv/bin/pip install -r requirements.txt

COPY script.py script.py

CMD [".venv/bin/python", "script.py"]
```

:information_source: If you are using [Enapter
Gateway](https://handbook.enapter.com/software/gateway_software/) and running
Linux, you should connect your containers to `host` network
:information_source::

```bash
docker run --network host ...
```
