import pygame

from components.collistion_component import CollisionComponent
from ecs_engine import ECSEngine
from entities.entity import Entity
from systems.collision_system import CollisionSystem
from systems.input_system import InputSystem
from systems.output_system import OutputSystem
from systems.rigitbody_system import RigitbodySystem
from components.move_component import MoveComponent
from components.input_component import InputComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent


def build_engine():
    engine = ECSEngine()
    player = Entity(1)
    transform = TransformComponent([20, 20])
    move = MoveComponent(20)
    rigitbody = RigidbodyComponent(1, 1)
    input = InputComponent()
    collision = CollisionComponent((10, 10))
    player.add_components([transform, move, input, rigitbody, collision])

    thing = Entity(2)
    transform = TransformComponent([100, 100])
    rigitbody = RigidbodyComponent(1, 1)
    collision = CollisionComponent((10, 10))
    thing.add_components([transform, rigitbody, collision])

    engine.add_entity(player)
    engine.add_entity(thing)

    engine.add_system(InputSystem)
    engine.add_system(CollisionSystem)
    engine.add_system(RigitbodySystem)
    engine.add_system(OutputSystem)
    return engine


ecs_engine = build_engine()
ecs_engine.run()
