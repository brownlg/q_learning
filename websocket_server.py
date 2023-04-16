import time
import asyncio
import websockets
import pyfirmata

board = pyfirmata.Arduino('COM5')


async def server(websocket, path):
    async for message in websocket:
        print("Received message:", message)

        # Process the
        if message == "ON":            
            board.digital[13].write(1)
        elif message == "OFF":
            board.digital[13].write(0)

        await websocket.send("Received message: " + message)
        

start_server = websockets.serve(server, "10.0.0.8", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
