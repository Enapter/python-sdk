# Standalone

## Basic Implementation

The most straightforward way to implement your own Standalone Device is this:

1. Subclass `enapter.standalone.Device`.
2. Override `async def run(self) -> None` method to send telemetry and properties.
3. Pass an instance of your device to `enapter.standalone.run`.

Here's a basic example:

```python
# my_device.py

import asyncio
import enapter

async def main():
    await enapter.standalone.run(MyDevice())

class MyDevice(enapter.standalone.Device):
    async def run(self):
        while True:
            await self.send_telemetry({})
            await self.send_properties({"model": "0.0.1"})
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
```

## Handling Commands

`enapter.standalone.Device` dispatches incoming command execution requests to
corresponding methods on your subclass.

If this command is defined in the manifest:

```yaml
configure_connection:
  display_name: Configure Connection
  group: connection
  arguments:
    ip_address:
      display_name: IP Address
      type: string
      required: true
    token:
      display_name: Bearer Authentication Token
      type: string
      required: false
```

This is the signature you would create in your device class to implement a
command handler:

```python
async def cmd_configure_connection(ip_address: str, token: str | None = None): ...
```

By default `cmd_` prefix is used to search the command handler.

## Synchronous Code

Blocking (CPU-bound) code should not be called directly. For example, if a
function performs a CPU-intensive calculation for 1 second, all concurrent
`asyncio` Tasks and IO operations would be delayed by 1 second.

Instead, use `asyncio.to_thread`:

```python
await asyncio.to_thread(blocking_call())
```

## Communication Config

> [!NOTE]
> The following instruction works only for v3 sites. If you have a v1 site,
> follow [this
> tutorial](https://developers.enapter.com/docs/tutorial/software-ucms/standalone)
> to generate your communication config.

Generate a communication config using [Enapter
CLI](https://github.com/Enapter/enapter-cli):

```bash
enapter3 device communication-config generate --device-id "$YOUR_DEVICE_ID" --protocol MQTTS | jq .config | base64 --wrap=0
```

</details>

## Running

Now you can use the communication config to run your device:

```bash
export ENAPTER_STANDALONE_COMMUNICATION_CONFIG="$YOUR_COMMUNICATION_CONFIG"
python my_device.py
```

## Running In Docker

Here's an example of a simple `Dockerfile`:

```Dockerfile
FROM python:3.13-alpine

WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt requirements.txt
RUN .venv/bin/pip install -r requirements.txt

COPY script.py script.py

CMD [".venv/bin/python", "script.py"]
```

> [!WARNING]
> If you are using Enapter Gateway and running Linux, you should connect your
> containers to the `host` network to make mDNS resolution work:
>
> ```bash
> docker run --network host ...
> ```
