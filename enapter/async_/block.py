import asyncio


async def block():
    never_happens = asyncio.Event()
    await never_happens.wait()
