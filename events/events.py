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
        self.entities_id = entities_id

    @property
    def entities_id(self):
        return self.__entities_id


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
