import time
import asyncio
import websockets

async def client():
    async with websockets.connect("ws://10.0.0.8:8765") as websocket:
        await websocket.send("Hello, world!")
        response = await websocket.recv()
        print("Received response:", response)


asyncio.get_event_loop().run_until_complete(client())
