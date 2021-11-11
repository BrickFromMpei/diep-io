from copy import deepcopy


class FireComponent:
    def __init__(self, rigitbody, health, damage, collision, cooldown, force, transform):
        self.__rigitbody = rigitbody
        self.__health = health
        self.__damage = damage
        self.cooldown = cooldown
        self.force = force
        self.__collision = collision
        self.__transform = transform
        self.timer = 0

    @property
    def rigitbody(self):
        return deepcopy(self.__rigitbody)

    @property
    def health(self):
        return deepcopy(self.__health)

    @property
    def damage(self):
        return deepcopy(self.__damage)

    @property
    def collision(self):
        return deepcopy(self.__collision)

    @property
    def transform(self):
        return deepcopy(self.__transform)

