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


def is_intersection(pos1, pos2, size1, size2):
    """Определяет, пересекаются ли 2 прямоугольника
        pos1, pos2 - координаты их центров
        size1, size2 - их разммеры"""
    collide = []
    for x1, x2, s1, s2 in zip(pos1, pos2, size1, size2):
        size = (s1 + s2) / 2
        if (x1 + size >= x2) and (x1 <= x2 + size):
            collide.append(True)
        else:
            collide.append(False)
    return all(collide)

