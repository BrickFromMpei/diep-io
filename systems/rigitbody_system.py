import time
from filters.filter import ComponentFilter, EventFilter
from events.events import CollisionEvent, MoveEvent, PositionUpdateEvent, CollisionStartEvent
from components.move_component import MoveComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent
from global_functions import find_by_id
from vector_fuctions import *


def set_new_velocities(collided, new_velocities):
    for i in new_velocities:
        collided[i][1].velocity = new_velocities[i]


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
        self.__collide_start_events = EventFilter(events, [CollisionStartEvent])
        self.__move_events = EventFilter(events, [MoveEvent])
        self.__delta_time = 0.0
        self.__start_time = time.time()
        # Коэффициент потери импульса при столкновении
        self.__collision_lost_coef = 0.9
        # Коэффициент силы с которой объекты будут друг друга выталкивать
        # при попадании друг в друга
        self.__resistance = 0.05

    def update(self):
        self.__delta_time = time.time() - self.__start_time
        self.__start_time = time.time()
        self.__collide_processing()
        self.__velocity_processing()
        self.__move_processing()

    def __collide_processing(self):
        self.__start_collide_processing()
        self.__current_collide_processing()

    def __start_collide_processing(self):
        for event in self.__collide_start_events:
            collided = self.__collided_component(event)
            new_velocities = {}
            for i in range(len(collided)):
                next_i = 0 if i == len(collided) - 1 else i + 1
                normal_vector = normal(collided[i][0], collided[next_i][0])
                velocity = collided[i][1].velocity
                if vector_len(velocity) > 0:
                    reflect_vector = reflect(velocity, normal_vector)
                    # Обмениваем импульсы между двумя столкнувшимися объектами
                    for x in [i, next_i]:
                        mass_coef = 1 - collided[x][1].mass / (collided[i][1].mass + collided[next_i][1].mass)
                        coef = mass_coef * self.__collision_lost_coef
                        new_velocity = [(-1)**(next_i - x + 1) * elem * coef for elem in reflect_vector]
                        if x in new_velocities:
                            for j in range(len(new_velocity)):
                                new_velocities[x][j] += new_velocity[j]
                        else:
                            new_velocities[x] = new_velocity
            set_new_velocities(collided, new_velocities)

    # Если объекты уже в состоянии коллизии, то мы из выталкиваем друг от друга
    def __current_collide_processing(self):
        for event in self.__collide_events:
            collided = self.__collided_component(event)
            for i in range(len(collided)):
                next_i = 0 if i == len(collided) - 1 else i + 1
                position_delta = vector_delta(collided[i][0].position,
                                              collided[next_i][0].position)
                velocity = collided[next_i][1].velocity
                for j in range(len(velocity)):
                    velocity[j] += position_delta[j] * self.__resistance

    def __collided_component(self, event):
        return [x.components for x in self.__entities if x.id in event.entities_id]

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
            entity = find_by_id(self.__move_entities, event.entity_id)
            direction = event.direction
            velocity = entity.components[1].velocity
            mass = entity.components[1].mass
            force = entity.components[0].force
            for i in range(len(direction)):
                accel = direction[i]*force / mass
                velocity[i] += accel * self.__delta_time

