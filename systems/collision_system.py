from events.events import CollisionEvent, CollisionStartEvent
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
        size = (size1[i] + size2[i]) / 2
        if ((position1[i] + size >= position2[i]) and
           (position1[i] <= position2[i] + size)):
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
        collided = [x.id for x in self.__collision_filter(True)]
        for entity in self.__entities:
            entity.components[1].in_collision = False
        for entity in self.__collision_filter(False):
            for entity2 in self.__collision_filter(False):
                # Искллючаем повторное добавление обной пары объектов
                if entity.id == entity2.id:
                    continue
                if pair_collision(entity, entity2):
                    entity.components[1].in_collision = True
                    entity2.components[0].in_collision = True
                    if not (entity.id in collided or entity2.id in collided):
                        self.__events.append(CollisionStartEvent([entity.id, entity2.id]))
                    self.__events.append(CollisionEvent([entity.id, entity2.id]))

    def __collision_filter(self, flag):
        for entity in self.__entities:
            if entity.components[1].in_collision == flag:
                yield entity
