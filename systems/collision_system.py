from events.events import CollisionEvent
from filters.filter import ComponentFilter, EventFilter
from components.transform_component import TransformComponent
from components.collistion_component import CollisionComponent


def pair_collision(first_entity, second_entity):
    position1 = first_entity.components[0].position
    position2 = second_entity.components[0].position
    size1 = first_entity.components[1].size
    size2 = second_entity.components[1].size
    collide = []

    for i in range(len(position1)):  # Go throw all directions
        if (position1[i] + size1[i] >= position2[i]) and \
           (position1[i] <= position2[i] + size2[i]):
            collide.append(True)
        else:
            collide.append(False)
    return min(collide)


class CollisionSystem:
    def __init__(self, entities, events):
        self.__entities = ComponentFilter(
            entities,
            [TransformComponent, CollisionComponent]
        )
        self.__events = events

    def update(self):
        ids = []
        for entity in self.__entities:
            for entity2 in self.__entities:
                # Искллючаем повторное добавление обной пары объектов
                if entity.id == entity2.id or [entity2.id, entity.id] in ids:
                    continue
                if pair_collision(entity, entity2):
                    ids.append([entity.id, entity2.id])
        for x in ids:
            self.__events.append(CollisionEvent([x[0], x[1]]))
