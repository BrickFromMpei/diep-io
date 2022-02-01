from events.events import CollisionEvent, CollisionStartEvent
from filters.filter import ComponentFilter, EventFilter
from components.transform_component import TransformComponent
from components.collistion_component import CollisionComponent
from global_functions import is_intersection


def pair_collision(first_entity, second_entity):
    position1 = first_entity.components[0].position
    position2 = second_entity.components[0].position
    size1 = first_entity.components[1].size
    size2 = second_entity.components[1].size
    return is_intersection(
        position1, position2, size1, size2
    )


class CollisionSystem:
    def __init__(self, entities, events):
        self.__entities = ComponentFilter(
            entities,
            [TransformComponent, CollisionComponent]
        )
        self.__events = events

    def update(self):
        collided = [x.id for x in self.__collision_filter(True)]
        self.__set_in_collision(False)

        for entity in self.__collision_filter(False):
            for entity2 in self.__collision_filter(False):
                # Искллючаем повторное добавление обной пары объектов
                if entity.id == entity2.id:
                    continue
                if pair_collision(entity, entity2):
                    self.__process_collision([entity, entity2], collided)

    def __process_collision(self, entities, collided):
        for entity in entities:
            entity.components[1].in_collision = True
        ids = [x.id for x in entities]
        if not any(x in collided for x in ids):
            self.__events.append(CollisionStartEvent(ids))
        self.__events.append(CollisionEvent(ids))

    def __set_in_collision(self, flag):
        for entity in self.__entities:
            entity.components[1].in_collision = flag

    def __collision_filter(self, flag):
        for entity in self.__entities:
            if entity.components[1].in_collision == flag:
                yield entity
