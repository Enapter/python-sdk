import asyncio

from enapter import cli

app = cli.App.new()
asyncio.run(app.run())
