import asyncio


class ECSEngine:
    def __init__(self):
        self.__entities = []
        self.__events = []
        self.__systems = []
        self.__running = True

    async def add_system(self, system):
        sys = system(self.__entities, self.__events)
        await sys.start()
        self.__systems.append(sys)

    def add_entity(self, entity):
        self.__entities.append(entity)

    async def run(self):
        while self.__running:
            self.__events.clear()
            for system in self.__systems:
                system.update()
            await asyncio.sleep(0)

    def stop(self):
        self.__running = False
