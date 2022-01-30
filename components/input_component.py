import websocket
import asyncio
import threading
import time


class InputComponent:
    def __init__(self, websocket):
        self.__is_running = True
        self.__ws = websocket

    async def run(self):
        async for message in self.__ws:
            self.__read_message(message)

    def update(self):
        pass

    def stop(self):
        self.__is_running = False

    def __read_message(self, message):
        print(message)
