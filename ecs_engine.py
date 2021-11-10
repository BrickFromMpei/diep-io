class ECSEngine:
    def __init__(self):
        self.__entities = []
        self.__events = []
        self.__systems = []
        self.__running = True

    def add_system(self, system):
        self.__systems.append(system(self.__entities,
                                     self.__events))

    def add_entity(self, entity):
        self.__entities.append(entity)

    def run(self):
        while self.__running:
            self.__events.clear()
            for system in self.__systems:
                system.update()

    def stop(self):
        self.__running = False
