def find_by_id(items, identifier):
    for item in items:
        if item.id == identifier:
            return item
    return None