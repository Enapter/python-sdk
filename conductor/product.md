# Initial Concept
A software development kit (SDK) for building applications and integrations with Enapter using Python.

## Target Audience
- Python Developers building custom applications for energy management.
- System Integrators connecting third-party systems to the Enapter platform.
- Hardware manufacturers integrating their devices into the Enapter ecosystem.

## Core Features
- **Standalone Devices Framework:** Tools and utilities for developing standalone device integrations.
- **MQTT API Client:** Seamless communication with the Enapter MQTT broker for real-time device control and telemetry data.
- **HTTP API Client:** Easy-to-use client for interacting with the Enapter Cloud HTTP API to manage sites, devices, historical data, and the Rule Engine.

## Key Goals
- Provide an idiomatic, modern Python 3.11+ interface for the Enapter ecosystem.
- Simplify authentication, networking, and error handling so developers can focus on business logic.
- Offer comprehensive examples and reliable asynchronous operations via tools like `aiomqtt` and `httpx`.
