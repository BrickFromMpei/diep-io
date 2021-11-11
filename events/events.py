class MoveEvent:
    def __init__(self, entity_id, direction):
        self.__entity_id = entity_id
        self.__direction = direction

    @property
    def entity_id(self):
        return self.__entity_id

    @property
    def direction(self):
        return self.__direction[:]


class CollisionEvent:
    def __init__(self, entities_id):
        self.__entities_id = entities_id

    @property
    def entities_id(self):
        return self.__entities_id[:]


class CollisionStartEvent(CollisionEvent):
    pass


class PositionUpdateEvent:
    def __init__(self, entity_id, position):
        self.__entity_id = entity_id
        self.__position = position

    @property
    def position(self):
        return self.position[:]

    @property
    def entity_id(self):
        return self.__entity_id


class FireEvent:
    def __init__(self, entity_id, target):
        self.__entity_id = entity_id
        self.__target = target

    @property
    def entity_id(self):
        return self.__entity_id

    @property
    def target(self):
        return self.__target[:]
