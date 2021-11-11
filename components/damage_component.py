class DamageComponent:
    def __init__(self, damage):
        self.__damage = damage

    @property
    def damage(self):
        return self.__damage
