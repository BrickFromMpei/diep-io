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
from systems.rigitbody_system import RigitbodySystem
from components.move_component import MoveComponent
from components.input_component import InputComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent


def build_engine():
    engine = ECSEngine()
    player = Entity(IdGenerator().get_next())
    transform = TransformComponent([20, 20])
    move = MoveComponent(100)
    rigitbody = RigidbodyComponent(1, 1, 0.1)
    input = InputComponent()
    collision = CollisionComponent((10, 10))
    health = HealthComponent(500)
    damage = DamageComponent(1)
    fire = fire_builder()
    player.add_components([transform, move, input, rigitbody, collision, health, damage, fire])

    thing = Entity(IdGenerator().get_next())
    transform = TransformComponent([100, 100])
    rigitbody = RigidbodyComponent(1, 1, 0.1)
    collision = CollisionComponent((10, 10))
    health = HealthComponent(100)
    thing.add_components([transform, rigitbody, collision, health])

    thing2 = Entity(IdGenerator().get_next())
    transform = TransformComponent([150, 100])
    rigitbody = RigidbodyComponent(1, 1, 0.1)
    collision = CollisionComponent((10, 10))
    health = HealthComponent(100)
    thing2.add_components([transform, rigitbody, collision, health])

    thing3 = Entity(IdGenerator().get_next())
    transform = TransformComponent([150, 150])
    rigitbody = RigidbodyComponent(1, 1, 0.1)
    collision = CollisionComponent((10, 10))
    health = HealthComponent(100)
    thing3.add_components([transform, rigitbody, collision, health])

    engine.add_entity(player)
    engine.add_entity(thing)
    engine.add_entity(thing2)
    engine.add_entity(thing3)

    engine.add_system(InputSystem)
    engine.add_system(FireSystem)
    engine.add_system(CollisionSystem)
    engine.add_system(HealthSystem)
    engine.add_system(RigitbodySystem)
    engine.add_system(OutputSystem)
    return engine


def fire_builder():
    rigitbody = RigidbodyComponent(0.002, 0.01, 0.0)
    collision = CollisionComponent([1, 1])
    health = HealthComponent(100)
    damage = DamageComponent(50)
    transform = TransformComponent([0, 0], (3, 3))
    force = 700
    cooldown = 1
    fire_component = FireComponent(rigitbody=rigitbody,
                                   collision=collision,
                                   health=health,
                                   damage=damage,
                                   force=force,
                                   cooldown=cooldown,
                                   transform=transform)
    return fire_component


ecs_engine = build_engine()
ecs_engine.run()
