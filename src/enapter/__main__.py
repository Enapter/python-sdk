import asyncio

from enapter import cli

app = cli.App.new()
try:
    asyncio.run(app.run())
except KeyboardInterrupt:
    pass
