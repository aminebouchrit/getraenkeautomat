#!/usr/bin/env python

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        if message == "Ping":
            message = "Pong"
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 80):
        await asyncio.Future()  # run forever

asyncio.run(main())