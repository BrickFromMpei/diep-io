class Entity:
    def __init__(self, id):
        self.__id = id
        self.__components = []

    @property
    def components(self):
        return self.__components

    @property
    def id(self):
        return self.__id

    def add_components(self, components):
        self.__components = components

    def remove_components(self, component):
        self.__components.remove(component)
