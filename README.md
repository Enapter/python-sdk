# Enapter Python SDK

[![CI](https://github.com/Enapter/python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/Enapter/python-sdk/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/enapter.svg)](https://pypi.org/project/enapter)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

A software development kit (SDK) for building applications and integrations
with Enapter using Python.

## Features

- [Standalone
  Devices](https://v3.developers.enapter.com/docs/standalone/introduction)
  framework
- [MQTT
  API](https://v3.developers.enapter.com/reference/device_integration/mqtt_api/)
  client
- [HTTP API](https://v3.developers.enapter.com/reference/http/intro) client

## Installation

> [!IMPORTANT]
> Requires **Python 3.11+**.

> [!WARNING]
> The API is still under development and may change at any time. It is
> recommended to pin the package version when installing.

Install from PyPI:

```bash
pip install enapter==0.14.0-rc2
```

## Usage

Explore the examples:

- [Standalone Devices](examples/standalone)
- [MQTT API](examples/mqtt/api)
- [HTTP API](examples/http/api)

These provide a good overview of the available features and should give you
enough to get started.

> [!TIP]
> Don't hesitate to peek into the source code - it's meant to be easy to
> follow.

## Help

If you feel lost or confused, reach us on
[Discord](https://discord.com/invite/TCaEZs3qpe) or just [file a
bug](https://github.com/Enapter/python-sdk/issues/new). We'd be glad to help.
