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
        self.__start_time = time.perf_counter()

    def update(self):
        self.__delta_time = time.perf_counter() - self.__start_time
        self.__start_time = time.perf_counter()
        self.__update_fire_timer()

        for event in self.__events:
            self.__process_event(event)

    def __process_event(self, event):
        entity = find_by_id(self.__entities, event.entity_id)
        fire_component = entity.components[1]
        if fire_component.timer <= 0:
            position = entity.components[0].position
            bullet = Entity(IdGenerator().get_next())
            target = event.target
            delta_pos = [x - y for x, y in zip(target, position)]
            delta_pos_len = sum(x ** 2 for x in delta_pos) ** .5
            delta_pos = [x / delta_pos_len for x in delta_pos]
            # 20 это размер коллайдера объекта
            # TODO: Переделать константу 20
            bullet_pos = [x + y * 20 for x, y in zip(position, delta_pos)]
            bullet = self.__buid_bullet(
                fire_component, bullet_pos, delta_pos
            )
            self.__all_entities.append(bullet)
            fire_component.timer = fire_component.cooldown

    def __update_fire_timer(self):
        for entity in self.__entities:
            fire_component = entity.components[1]
            if fire_component.timer > 0:
                fire_component.timer -= self.__delta_time

    def __buid_bullet(self, fire_component, position, delta_position):
        transform = fire_component.transform
        transform.position = position
        rigitbody = fire_component.rigitbody
        health = fire_component.health
        collision = fire_component.collision
        damage = fire_component.damage
        force = fire_component.force
        bullet = Entity(IdGenerator().get_next())
        bullet.add_components([
            transform, rigitbody, health, collision, damage
        ])
        self.__fire_bullet(
            bullet, force, delta_position, rigitbody
        )
        return bullet

    def __fire_bullet(self, bullet, force, delta_position, rigitbody):
        for i in range(len(delta_position)):
            # Работает НЕ через ускорение, т.к приложенаая сила
            # моментальна и не действует долговременно
            add_velocity = delta_position[i] * force / rigitbody.mass
            rigitbody.velocity[i] += add_velocity
