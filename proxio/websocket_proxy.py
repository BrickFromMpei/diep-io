import asyncio
import websockets
from . import input_messages, output_messages


class WebsocketProxy:
    def __init__(self):
        self.__PORT = '6789'
        self.__connected = []

    async def start(self):
        await websockets.serve(self.__listen_socket, "localhost", self.__PORT)

    async def __listen_socket(self, websocket):
        print("A client just connected")
        self.__connected.append(websocket)
        try:
            async for message in websocket:
                print("Received message from client: " + message)
        except websockets.exceptions.ConnectionClosed as e:
            print("A client just disconnected")
            self.__connected.remove(websocket)

    async def __send_message(self, message):
        for socket in self.__connected:
            try:
                await socket.send("Someone said: " + message)
            except websockets.exceptions.ConnectionClosed as e:
                self.__connected.remove(socket)

    async def update_event_loop(self):
        for message in output_messages:
            await self.__send_message(message)
            output_messages.remove(message)

