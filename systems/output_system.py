from components.input_component import InputComponent
from components.transform_component import TransformComponent
from filters.filter import ComponentFilter
import proxio


class OutputSystem:
    def __init__(self, entities, events):
        self.__entities = ComponentFilter(
            entities,
            [TransformComponent]
        )
        self.__events = events
        self.__players = ComponentFilter(
            entities,
            [InputComponent]
        )

    def update(self):
        proxio.output_messages.append("hi")
