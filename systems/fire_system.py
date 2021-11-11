import time

from components.fire_component import FireComponent
from components.transform_component import TransformComponent
from entities.entity import Entity
from events.events import FireEvent
from filters.filter import ComponentFilter, EventFilter
from global_functions import find_by_id
from id_generator import IdGenerator


class FireSystem:
    def __init__(self, entities, events):
        self.__entities = ComponentFilter(
            entities,
            [TransformComponent, FireComponent]
        )
        self.__events = EventFilter(
            events,
            [FireEvent]
        )
        self.__all_entities = entities
        # TODO сделать глобальный таймер
        self.__delta_time = 0.0
        self.__start_time = time.time()

    def update(self):
        self.__delta_time = time.time() - self.__start_time
        self.__start_time = time.time()
        for entity in self.__entities:
            fire_component = entity.components[1]
            if fire_component.timer > 0:
                fire_component.timer -= self.__delta_time

        for event in self.__events:
            entity = find_by_id(self.__entities, event.entity_id)
            fire_component = entity.components[1]
            if fire_component.timer <= 0:
                position = entity.components[0].position
                bullet = Entity(IdGenerator().get_next())
                target = event.target
                delta_position = []
                for i in range(len(position)):
                    delta_position.append(target[i] - position[i])
                delta_position_len = sum(x**2 for x in delta_position)**.5
                delta_position = [x/delta_position_len for x in delta_position]
                bullet_position = []
                for i in range(len(position)):
                    # 10 это размер коллайдера объекта
                    # TODO: Переделать константу 10
                    bullet_position.append(position[i] + delta_position[i]*10)

                transform = fire_component.transform
                transform.position = bullet_position
                rigitbody = fire_component.rigitbody
                health = fire_component.health
                collision = fire_component.collision
                damage = fire_component.damage
                bullet.add_components([transform,
                                       rigitbody,
                                       health,
                                       collision,
                                       damage])

                force = fire_component.force
                for i in range(len(delta_position)):
                    accel = delta_position[i] * force / rigitbody.mass
                    rigitbody.velocity[i] += accel * self.__delta_time  # TODO сделать глобальный таймер
                self.__all_entities.append(bullet)
                fire_component.timer = fire_component.cooldown
