import time
from filters.filter import filter_entities, filter_events
from events.events import CollisionEvent, MoveEvent, PositionUpdateEvent
from components.move_component import MoveComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponents


class RigitBodySystem:
    def __init__(self, entities, events):
        self.__entities = filter_entities(
            entities,
            [TransformComponents, RigidbodyComponent]
        )
        self.__move_entities = filter_entities(
            entities,
            [MoveComponent, RigidbodyComponent]
        )
        self.__events = events
        self.__collide_events = filter_events(events, CollisionEvent)
        self.__move_events = filter_events(events, MoveEvent)
        self.__delta_time = time.time()

    def update(self):
        self.__delta_time = time.time() - self.__delta_time
        self.__collide_processing()
        self.__velocity_processing()
        self.__move_processing()

    def __collide_processing(self):
        for event in self.__collide_events:
            collided = [x[1] for x in self.__entities if x.id in event.entities_id]
            for i in range(len(collided)):
                next_i = 0 if i == len(collided) - 1 else i + 1
                impulse = [x*collided[i].mass for x in collided[i].velocity]
                velocity = [x/collided[next_i].mass for x in impulse]
                collided[next_i].veloity = velocity

    def __velocity_processing(self):
        for entity in self.__entities:
            velocity = entity[1].velocity
            position = entity[0].position
            if velocity != [0, 0]:
                for i in range(len(velocity)):  # Go throw all directions
                    position[i] += velocity[i] * self.__delta_time
                self.__events.append(PositionUpdateEvent(entity.id, position))

    def __move_processing(self):
        for event in self.__move_events:
            for entity in filter(lambda i: i.id == event.id, self.__move_entities):
                direction = event.direction
                velocity = entity[1].velocity
                mass = entity[1].maxx
                force = entity[0].force
                for i in range(len(direction)):
                    accel = direction[i]*force[i] / mass
                    velocity[i] += accel * self.__delta_time

