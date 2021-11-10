import time
from filters.filter import ComponentFilter, EventFilter
from events.events import CollisionEvent, MoveEvent, PositionUpdateEvent
from components.move_component import MoveComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent


class RigitbodySystem:
    def __init__(self, entities, events):
        self.__entities = ComponentFilter(
            entities,
            [TransformComponent, RigidbodyComponent]
        )
        self.__move_entities = ComponentFilter(
            entities,
            [MoveComponent, RigidbodyComponent]
        )
        self.__events = events
        self.__collide_events = EventFilter(events, [CollisionEvent])
        self.__move_events = EventFilter(events, [MoveEvent])
        self.__delta_time = 0.0
        self.__start_time = time.time()

    def update(self):
        print("Delta Time %s" % self.__delta_time) # TODO log
        self.__delta_time = time.time() - self.__start_time
        self.__start_time = time.time()
        self.__collide_processing()
        self.__velocity_processing()
        self.__move_processing()

    def __collide_processing(self):
        for event in self.__collide_events:
            collided = [x.components for x in self.__entities if x.id in event.entities_id]
            new_velocities = {}
            for i in range(len(collided)):
                next_i = 0 if i == len(collided) - 1 else i + 1
                position = collided[i][0].position
                next_position = collided[next_i][0].position
                position_delta = []
                velocity = collided[i][1].velocity
                for j in range(len(position)):
                    position_delta.append(next_position[j] - position[j])
                scalar = sum(velocity[i] * position_delta[i] for i in range(len(velocity)))
                if scalar >= 0:
                    impulse = [x*collided[i][1].mass for x in velocity]
                    new_velocity = [x/collided[next_i][1].mass for x in impulse]
                    new_velocities[next_i] = new_velocity

            for i in new_velocities:
                collided[i][1].velocity = new_velocities[i]

    def __velocity_processing(self):
        for entity in self.__entities:
            velocity = entity.components[1].velocity
            position = entity.components[0].position
            friction = entity.components[1].friction
            if velocity != [0, 0]:
                for i in range(len(velocity)):  # Go throw all directions
                    position[i] += velocity[i] * self.__delta_time

                for i in range(len(velocity)):
                    velocity[i] *= 1/(1 + friction * self.__delta_time)
                self.__events.append(PositionUpdateEvent(entity.id, position))

    def __move_processing(self):
        for event in self.__move_events:
            for entity in filter(lambda i: i.id == event.entity_id, self.__move_entities):  # TODO Фильтре не фильтрует, возвращет все элементы
                direction = event.direction
                velocity = entity.components[1].velocity
                print("Velocity %s" % velocity)  # TODO log
                mass = entity.components[1].mass
                force = entity.components[0].force
                for i in range(len(direction)):
                    accel = direction[i]*force / mass
                    velocity[i] += accel * self.__delta_time

