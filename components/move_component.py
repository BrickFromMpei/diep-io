class MoveComponent:
    def __init__(self, force):
        self.__force = force

    @property
    def force(self):
        return self.__force

