class TransformComponent:
    def __init__(self, position, size=(10, 10)):
        self.__position = position
        self.__size = size

    @property
    def position(self):
        return self.__position

    @property
    def size(self):
        return self.__size[:]

    @position.setter
    def position(self, position):
        self.__position = position
