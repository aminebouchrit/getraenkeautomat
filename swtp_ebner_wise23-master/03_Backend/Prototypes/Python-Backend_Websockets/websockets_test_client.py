#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:80") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello())


#make use of internat test client that comes with websockets package
# python -m websockets ws://localhost:80/