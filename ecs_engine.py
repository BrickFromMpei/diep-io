import asyncio


class ECSEngine:
    def __init__(self):
        self.__entities = []
        self.__events = []
        self.__systems = []
        self.__proxy = None
        self.__running = True

    def add_system(self, system):
        self.__systems.append(system(self.__entities,
                                     self.__events))

    def add_entity(self, entity):
        self.__entities.append(entity)

    def add_proxy(self, proxy):
        self.__proxy = proxy

    async def run(self):
        await self.__proxy.start()
        while self.__running:
            await self.__proxy.update_event_loop()
            self.__events.clear()
            for system in self.__systems:
                system.update()

    def stop(self):
        self.__running = False
