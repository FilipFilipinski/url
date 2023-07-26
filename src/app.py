from aiohttp import web
from loguru import logger

from src.context.main import Context

"""
Standalone aiohttp app launcher.

Should only an (instantiated) app:web.Application be needed -- use logic as in `async_async_app_factory`.

"""


async def async_app_factory():
    context = Context()
    await context.initialize()
    return context.app()


def run_server():
    logger.info("Starting HTTP listener on port 8080..")
    web.run_app(async_app_factory(), port=8080)


if __name__ == "__main__":
    run_server()
