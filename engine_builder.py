import config
import random
from global_functions import is_intersection
from components.collistion_component import CollisionComponent
from components.damage_component import DamageComponent
from components.fire_component import FireComponent
from components.health_component import HealthComponent
from ecs_engine import ECSEngine
from entities.entity import Entity
from id_generator import IdGenerator
from systems.collision_system import CollisionSystem
from systems.fire_system import FireSystem
from systems.health_system import HealthSystem
from systems.input_system import InputSystem
from systems.output_system import OutputSystem
from components.move_component import MoveComponent
from components.input_component import InputComponent
from systems.rigitbody_system import RigitbodySystem
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent


class EngineBuilder:
    """
        Данный класс создаёт новый экземплят игрового мира
    """
    def __init__(self):
        self.__engine = ECSEngine()

    def build(self):
        self.__add_obstacles()
        self.__add_player()
        self.__add_systems()
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

    def __add_systems(self):
        self.__engine.add_system(InputSystem)
        self.__engine.add_system(FireSystem)
        self.__engine.add_system(CollisionSystem)
        self.__engine.add_system(HealthSystem)
        self.__engine.add_system(RigitbodySystem)
        self.__engine.add_system(OutputSystem)

    def __add_player(self):
        player = self.__create_player()
        self.__engine.add_entity(player)

    def __create_player(self):
        player = Entity(IdGenerator().get_next())
        transform = TransformComponent([10,10], config.PLAYER_SIZE)
        move = MoveComponent(config.PLAYER_MOVE_FORCE)
        rigitbody = RigidbodyComponent(config.PLAYER_MASS, config.FRICTION)
        input = InputComponent()
        collision = CollisionComponent(config.PLAYER_SIZE)
        health = HealthComponent(config.PLAYER_HEALTH)
        damage = DamageComponent(config.PLAYER_BODY_DAMAGE)
        fire = self.__create_fire()
        player.add_components(
            [transform, move, input, rigitbody,
             collision, health, damage, fire]
        )
        return player

    def __create_fire(self):
        rigitbody = RigidbodyComponent(0.002, 0.01)
        collision = CollisionComponent(config.BULLET_SIZE)
        health = HealthComponent(2)
        damage = DamageComponent(50)
        transform = TransformComponent([0, 0], config.BULLET_SIZE)
        force = 0.3
        cooldown = 1
        fire_component = FireComponent(rigitbody=rigitbody,
                                       collision=collision,
                                       health=health,
                                       damage=damage,
                                       force=force,
                                       cooldown=cooldown,
                                       transform=transform)
        return fire_component
