class CollisionComponent:
    def __init__(self, size):
        self.__size = size
        self.in_collision = False

    @property
    def size(self):
        return self.__size

    @property
    def layer(self):
        return self.__layer
