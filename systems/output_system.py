import pygame
from components.transform_component import TransformComponent
from filters.filter import ComponentFilter, EventFilter



def init_screen():
    background_colour = (255, 255, 255)
    (width, height) = (700, 700)
    screen = pygame.display.set_mode((width, height))
    screen.fill(background_colour)
    pygame.display.flip()
    return screen


class OutputSystem:
    def __init__(self, entities, events):
        self.__entities = ComponentFilter(
            entities,
            [TransformComponent]
        )
        self.__events = events
        self.__screen = init_screen()

    def update(self):
        self.__screen.fill((255, 255, 255))
        for entity in self.__entities:
            size = entity.components[0].size
            pygame.draw.rect(self.__screen, (0, 0, 0),
                             (int(entity.components[0].position[0]) - size[0],
                             int(entity.components[0].position[1]) - size[1],
                             size[0], size[1])
                             )

        pygame.display.flip()
