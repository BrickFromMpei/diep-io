from engine_builder import EngineBuilder


def start():
    builder = EngineBuilder()
    ecs_engine = builder.build()
    ecs_engine.run()


if __name__ == "__main__":
    start()