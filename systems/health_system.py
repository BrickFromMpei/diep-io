from components.damage_component import DamageComponent
from components.health_component import HealthComponent
from events.events import CollisionEvent, CollisionStartEvent
from filters.filter import ComponentFilter, EventFilter
from global_functions import find_by_id


class HealthSystem:
    def __init__(self, entities, events):
        self.__all_entities = entities
        self.__entities_with_health = ComponentFilter(
            entities,
            [HealthComponent]
        )
        self.__entities_with_damage = ComponentFilter(
            entities,
            [DamageComponent]
        )
        self.__events = EventFilter(
            events,
            [CollisionStartEvent]
        )

    def update(self):
        for event in self.__events:
            ids = event.entities_id
            for i in range(len(ids)):
                next_i = i + 1 if i < len(ids) - 1 else 0
                if ids[next_i] in [x.id for x in self.__entities_with_health]:
                    health_entity = find_by_id(self.__entities_with_health, ids[next_i])
                    if ids[i] in [x.id for x in self.__entities_with_damage]:
                        damage_entity = find_by_id(self.__entities_with_damage, ids[i])
                        health_entity.components[0].health -= damage_entity.components[0].damage
            for entity in self.__entities_with_health:
                if entity.components[0].health < 0:
                    entity_to_remove = find_by_id(self.__all_entities, entity.id)
                    self.__all_entities.remove(entity_to_remove)



