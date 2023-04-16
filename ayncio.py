import asyncio

class MyClass2:
    def __init__(self) -> None:
        self.queue = asyncio.Queue()

    async def handle_message(self, message):
        # handle the message here
        print("Received message:", message)

    async def listen_for_messages(self):
        while True:
            message = await self.queue.get()
            await self.handle_message(message)

    async def start(self):
        # start listening for messages in the background
        asyncio.create_task(self.listen_for_messages())

    async def send_message(self, message):
        # send a message to MyClass2
        await self.queue.put(message)
