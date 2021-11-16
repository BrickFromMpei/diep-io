from entities.entity import Entity


class EventFilter:
    def __init__(self, events, types):
        self.__events = events
        self.__types = types

    def __iter__(self):
        return self.__filter_events()

    def __filter_events(self):
        for event in self.__events:
            if any([isinstance(event, x) for x in self.__types]):
                yield event


class ComponentFilter:
    def __init__(self, entities, types):
        self.__entities = entities
        self.__types = types

    def __iter__(self):
        return self.__filter_entities()

    def __filter_entities(self):
        for entity in self.__entities:
            mapped_components = self.__map_components(entity.components)
            if len(mapped_components) > 0:
                entity_to_return = Entity(entity.id)
                entity_to_return.add_components(mapped_components)
                yield entity_to_return

    def __map_components(self, components):
        components_to_return = []
        for tp in self.__types:
            for component in components:
                if isinstance(component, tp):
                    components_to_return.append(component)
        if len(components_to_return) == len(self.__types):
            return components_to_return
        return []


