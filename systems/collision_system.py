from events.events import CollisionEvent
from filters.filter import filter_entities
from components.transform_component import TransformComponents
from components.collistion_component import CollisionComponent


def pair_collision(first_entity, second_entity):
    position1 = first_entity[0].position
    position2 = second_entity[0].position
    size1 = first_entity[1].size
    size2 = second_entity[2].size
    collide = []

    for i in range(len(position1)):  # Go throw all directions
        if (position1[i] + size1[i] >= position2[i]) and \
           (position1[i] <= position2[i] + size2[i]):
            collide.append(True)
        else:
            collide.append(False)
    return min(collide)


class CollisionSystem:
    def __init__(self, events):
        self.__entities = filter_entities(
            events,
            [TransformComponents, CollisionComponent]
        )
        self.__events = events

    def update(self):
        for entity in self.__entities:
            for entity2 in self.__entities:
                if entity == entity:
                    continue
                if pair_collision(entity, entity2):
                    self.__events.append(CollisionEvent([entity, entity2]))
