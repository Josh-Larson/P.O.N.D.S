#!/usr/bin/env python

import asyncio
import websockets

async def echo(websocket, path):
    while True:
    message = yield from websocket.recv()
        await websocket.send(message)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()