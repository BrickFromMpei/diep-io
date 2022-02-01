import asyncio
from engine_builder import EngineBuilder


async def start():
    builder = EngineBuilder()
    ecs_engine = builder.build()
    await ecs_engine.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.run_forever()
