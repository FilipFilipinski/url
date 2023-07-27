from aiohttp import web
from loguru import logger

from src.helpers.middlewares.jsonify_response import jsonify_middleware


async def setup_middlewares(app: web.Application):
    logger.info("Initializing middlewares...")

    app.middlewares.append(jsonify_middleware)
