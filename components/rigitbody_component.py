class RigidbodyComponent:
    def __init__(self, mass: float, friction: float, resistance: float):
        if mass <= 0:
            raise ValueError("Масса должна быть положительной")
        self.__mass = mass
        self.__friction = friction
        self.__velocity = [0, 0]
        self.__resistance = resistance

    @property
    def mass(self):
        return self.__mass

    @property
    def friction(self):
        return self.__friction

    @property
    def velocity(self):
        return self.__velocity

    @property
    def resistance(self):
        return self.__resistance

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = velocity
