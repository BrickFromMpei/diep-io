import config
import websockets
import asyncio
from id_generator import IdGenerator
from entities.entity import Entity
from components.move_component import MoveComponent
from components.fire_component import FireComponent
from components.input_component import InputComponent
from components.collistion_component import CollisionComponent
from components.damage_component import DamageComponent
from components.health_component import HealthComponent
from components.rigitbody_component import RigidbodyComponent
from components.transform_component import TransformComponent
from filters.filter import ComponentFilter
from systems.isystem import ISystem


class InputSystem(ISystem):
    def __init__(self, entities, events):
        self.__PORT = 6789
        self.__running = True
        self.__events = events
        self.__connected = []
        self.__entities = entities
        self.__players = ComponentFilter(
            entities,
            [InputComponent]
        )

    async def start(self):
        await websockets.serve(self.__add_player, "localhost", self.__PORT)

    async def __add_player(self, websocket, path):
       player = await self.__create_player(websocket)
       self.__entities.append(player)

    def update(self):
        for player in self.__players:
            player.components[0].update()

    async def __create_player(self, websocket):
        player = Entity(IdGenerator().get_next())
        transform = TransformComponent([10, 10], config.PLAYER_SIZE)
        move = MoveComponent(config.PLAYER_MOVE_FORCE)
        rigitbody = RigidbodyComponent(config.PLAYER_MASS, config.FRICTION)
        input = InputComponent(websocket)
        await input.run()
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
