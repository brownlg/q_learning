import pyfirmata
import time

import asyncio
import websockets


board = pyfirmata.Arduino('COM5')

async def server(websocket, path):
    async for message in websocket:
        print("Received message:", message)
        await websocket.send("Received message: " + message)

start_server = websockets.serve(server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


# while True:
#     board.digital[13].write(1)
#     time.sleep(5)
#     board.digital[13].write(0)
#     time.sleep(5)