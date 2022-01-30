import config
import random
from global_functions import is_intersection
from components.collistion_component import CollisionComponent
from components.damage_component import DamageComponent
from components.health_component import HealthComponent
from ecs_engine import ECSEngine
from entities.entity import Entity
from id_generator import IdGenerator
from systems.collision_system import CollisionSystem
from systems.fire_system import FireSystem
from systems.health_system import HealthSystem
from systems.input_system import InputSystem
from systems.output_system import OutputSystem
from systems.rigitbody_system import RigitbodySystem
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent


class EngineBuilder:
    """
        Данный класс создаёт новый экземплят игрового мира
    """
    def __init__(self):
        self.__engine = ECSEngine()

    async def build(self):
        self.__add_obstacles()
        await self.__add_systems()
        return self.__engine

    def __add_obstacles(self):
        for i in range(config.OBSTACLE_COUNT):
            position, size = self.__create_obstacle_transform()
            health = random.randint(
                config.MIN_OBSTACLE_HEALTH,
                config.MAX_OBSTACLE_HEALTH
            )
            mass = random.randint(
                config.MIN_OBSTACLE_MASS,
                config.MAX_OBSTACLE_MASS
            )
            self.__engine.add_entity(
                self.__create_obstacle(
                    position, size, health, mass,
                    config.FRICTION, config.OBSTACLE_DAMAGE
                )
            )

    def __create_obstacle_transform(self):
        is_correct_transform = False
        position = []
        size = ()
        while not is_correct_transform:
            size_x = random.randint(
                config.MIN_OBSTACLE_SIZE, config.MAX_OBSTACLE_SIZE
            )
            size_y = random.randint(
                config.MIN_OBSTACLE_SIZE, config.MAX_OBSTACLE_SIZE
            )
            size = (size_x, size_y)
            position = [random.randint(0, x) for x in config.FIELD_SIZE]
            intersections = []
            for zone in config.SAFE_ZONES:
                zone_position = zone[0]
                zone_size = zone[1]
                intersections.append(
                    is_intersection(
                        zone_position, position, zone_size, size
                    )
                )
            is_correct_transform = not all(intersections)
        return position, size

    def __create_obstacle(self, position, size, health, mass, friction, damage):
        obstacle = Entity(IdGenerator().get_next())
        transform = TransformComponent(position, size)
        rigitbody = RigidbodyComponent(mass, friction)
        collision = CollisionComponent(size)
        damage_comp = DamageComponent(damage)
        health = HealthComponent(health)
        obstacle.add_components(
            [transform, rigitbody, collision, health, damage_comp]
        )
        return obstacle

    async def __add_systems(self):
        await self.__engine.add_system(InputSystem)
        await self.__engine.add_system(FireSystem)
        await self.__engine.add_system(CollisionSystem)
        await self.__engine.add_system(HealthSystem)
        await self.__engine.add_system(RigitbodySystem)
        await self.__engine.add_system(OutputSystem)


