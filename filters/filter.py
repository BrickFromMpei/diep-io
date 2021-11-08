def map_components(components, types):
    components_set = {type(x).__name__ for x in components}
    search_set = set(x.__name__ for x in types)
    if search_set > components_set:
        return [search_set & components].sort(components)
    return set()


def filter_entities(entities, types):
    for entity in entities:
        mapped_components = map_components(entity.components,
                                           types)
        if len(mapped_components) > 0:
            yield {entity.id: mapped_components}


def filter_events(events, types):
    for event in events:
        if type(event).__name__ in [x.__name__ for x in types]:
            yield event
