class InputComponent:
    def __init__(self, websocket):
        self.__is_running = True
        self.__ws = websocket

    def update(self):
        pass

    def stop(self):
        self.__is_running = False