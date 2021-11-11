import pygame
from events.events import MoveEvent, FireEvent
from filters.filter import ComponentFilter, EventFilter
from components.input_component import InputComponent


class InputSystem:
    def __init__(self, entities, events):
        self.__running = True
        self.__events = events
        self.__entities = ComponentFilter(
            entities,
            [InputComponent]
        )

    def update(self):
        direction = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            direction[0] -= 1
        if keys[pygame.K_RIGHT]:
            direction[0] += 1
        if keys[pygame.K_UP]:
            direction[1] -= 1
        if keys[pygame.K_DOWN]:
            direction[1] += 1
        if direction != [0, 0]:
            self.__events.append(MoveEvent(list(self.__entities)[0].id, direction))
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            self.__events.append(FireEvent(list(self.__entities)[0].id, (x, y)))
        pygame.event.pump()
