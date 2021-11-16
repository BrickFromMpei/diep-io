import time
from filters.filter import ComponentFilter, EventFilter
from events.events import CollisionEvent, MoveEvent, PositionUpdateEvent, CollisionStartEvent
from components.move_component import MoveComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent
from global_functions import find_by_id, by_pair
from vector_fuctions import *


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
        self.__collide_start_events = EventFilter(
            events, [CollisionStartEvent]
        )
        self.__move_events = EventFilter(events, [MoveEvent])
        self.__delta_time = 0.0
        self.__start_time = time.perf_counter()
        # Коэффициент потери импульса при столкновении
        self.__collision_lost_coef = 0.9
        # Коэффициент силы с которой объекты будут друг друга выталкивать
        # при попадании друг в друга
        self.__resistance = 0.05

    def update(self):
        self.__delta_time = time.perf_counter() - self.__start_time
        self.__start_time = time.perf_counter()
        self.__collide_processing()
        self.__velocity_processing()
        self.__move_processing()

    def __collide_processing(self):
        self.__start_collide_processing()
        self.__current_collide_processing()

    def __velocity_processing(self):
        for entity in self.__entities:
            dt = self.__delta_time
            components = entity.components
            velocity = components[1].velocity
            position = components[0].position
            friction = components[1].friction
            if velocity != [0, 0]:
                components[0].position = vector_sum(position, velocity, dt)
                coef = 1/(1 + friction * dt)
                components[1].velocity = vector_multiply(velocity, coef)
                self.__events.append(
                    PositionUpdateEvent(entity.id, position)
                )

    def __move_processing(self):
        for event in self.__move_events:
            entity = find_by_id(self.__move_entities, event.entity_id)
            direction = event.direction
            components = entity.components
            velocity = components[1].velocity
            mass = components[1].mass
            force = components[0].force
            coef = force/mass * self.__delta_time
            components[1].velocity = vector_sum(velocity, direction, coef)

    def __start_collide_processing(self):
        for event in self.__collide_start_events:
            collided = self.__collided_component(event)
            for primary, secondary in by_pair(collided):
                self.__reflect_velocity(primary, secondary)

    # Если объекты уже в состоянии коллизии,
    # то мы из выталкиваем друг от друга
    def __current_collide_processing(self):
        for event in self.__collide_events:
            collided = self.__collided_component(event)
            for collided1, collided2 in by_pair(collided):
                position_delta = vector_delta(
                    collided1[0].position, collided2[0].position
                )
                for elem in [collided1, collided2]:
                    velocity = elem[1].velocity
                    elem[1].velocity = vector_sum(
                        velocity, position_delta, self.__resistance
                    )

    def __collided_component(self, event):
        return [
            x.components for x in self.__entities if x.id in event.entities_id
        ]

    # Обмениваем импульсы между двумя столкнувшимися объектами
    def __reflect_velocity(self, primary, secondary):
        normal_vector = normal(primary[0], secondary[0])
        mass_sum = primary[1].mass + secondary[1].mass
        new_velocities = []
        for x, y in zip([primary, secondary], [secondary, primary]):
            mass = x[1].mass
            coef = 1 - mass / mass_sum
            velocity_sum = vector_sum(x[1].velocity, y[1].velocity, -1)
            reflect_vector = reflect(velocity_sum, normal_vector)
            new_velocities.append(
                vector_multiply(reflect_vector, coef)
            )
        for x, y in zip([primary, secondary], new_velocities):
            x[1].velocity = y

