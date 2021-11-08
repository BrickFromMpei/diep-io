class CollisionComponent:
    def __init__(self, size: tuple[int, int]):
        self.__size = size

    @property
    def size(self):
        return self.__size
