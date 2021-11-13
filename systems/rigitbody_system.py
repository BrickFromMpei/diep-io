import time
from filters.filter import ComponentFilter, EventFilter
from events.events import CollisionEvent, MoveEvent, PositionUpdateEvent, CollisionStartEvent
from components.move_component import MoveComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent


def vector_delta(vector1, vector2):
    check_vector(vector1, vector2)
    position_delta = []
    for j in range(len(vector1)):
        position_delta.append(vector2[j] - vector1[j])
    return position_delta


def set_new_velocities(collided, new_velocities):
    for i in new_velocities:
        collided[i][1].velocity = new_velocities[i]


def cos_angle(vector1, vector2):
    check_vector(vector1, vector2)
    scalar_value = scalar(vector1, vector2)
    return scalar_value / (vector_len(vector1) * vector_len(vector2))


def scalar(vector1, vector2):
    check_vector(vector1, vector2)
    return sum(vector1[i] * vector2[i] for i in range(len(vector1)))


def vector_len(vector):
    return sum(x**2 for x in vector)**.5


def reflect(vector, normal_vector):
    check_vector(vector, normal_vector)
    reflect_vector = []
    for x in normal_vector:
        reflect_vector.append(
            x*vector_len(vector)*cos_angle(vector, normal_vector)
        )
    return reflect_vector


#  TODO Пересчитать нормаль
def normal(transform1, transform2):
    check_vector(transform1.size, transform2.size)
    check_vector(transform1.position, transform1.size)
    check_vector(transform1.position, transform2.position)
    normal_vector = []
    for i in range(len(transform1.position)):
        size = transform1.size[i]/2 + transform2.size[i]/2
        pos_delta = transform1.position[i] - transform2.position[i]
        if abs(pos_delta) > size:
            normal_vector.append(0)
        else:
            if pos_delta - size > 0:
                normal_vector.append(1)
            else:
                normal_vector.append(-1)
    return normal_vector


def check_vector(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Length on vectors must be equal")


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

    def update(self):
        self.__delta_time = time.time() - self.__start_time
        self.__start_time = time.time()
        self.__collide_processing()
        self.__velocity_processing()
        self.__move_processing()

    def __collide_processing(self):
        self.__start_collide_processing()
        self.__current_collide_processing()

    # TODO переделать столкновения
    def __start_collide_processing(self):
        for event in self.__collide_start_events:
            collided = self.__collided_component(event)
            new_velocities = {}
            for i in range(len(collided)):
                next_i = 0 if i == len(collided) - 1 else i + 1
                normal_vector = normal(collided[i][0], collided[next_i][0])
                velocity = collided[i][1].velocity
                reflect_vector = reflect(velocity, normal_vector)
                impulse = [x*collided[i][1].mass for x in velocity]
                new_velocity = [x/collided[next_i][1].mass for x in impulse]
                new_velocities[next_i] = new_velocity
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
                resistance = collided[i][1].resistance
                for j in range(len(velocity)):
                    velocity[j] += position_delta[j] * resistance

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
            for entity in filter(lambda i: i.id == event.entity_id, self.__move_entities):  # TODO Фильтре не фильтрует, возвращет все элементы
                direction = event.direction
                velocity = entity.components[1].velocity
                mass = entity.components[1].mass
                force = entity.components[0].force
                for i in range(len(direction)):
                    accel = direction[i]*force / mass
                    velocity[i] += accel * self.__delta_time

