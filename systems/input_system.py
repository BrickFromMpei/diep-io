import pygame
from events.events import MoveEvent
from filters.filter import filter_entities
from components.input_component import InputComponent


class InputSystem:
    def __init__(self, events, entities):
        self.__running = True
        self.__events = events
        self.__entity = filter_entities(
            entities,
            [InputComponent]
        )[0]

    def update(self):
        while self.__running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.__events.append(MoveEvent(self.__entity.id, [1, 0]))
            pygame.event.pump()

    def stop(self):
        self.__running = False
