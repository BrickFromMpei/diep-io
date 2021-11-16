# TODO переделать список сущностей на класс
def find_by_id(items, identifier):
    for item in items:
        if item.id == identifier:
            return item
    return None

def by_pair(items):
    for i in range(0, len(items), 2):
        if i == len(items) - 1:
            break
        yield items[i], items[i+1]
