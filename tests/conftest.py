import asyncio
import os

import pytest
from dotenv import load_dotenv
from loguru import logger

from src.app import async_app_factory
from src.repos.user_repo import UserRepository
from src.service.database.dbpool import DBPool


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop_policy().get_event_loop()


@pytest.fixture(scope="session")
async def app():
    return await async_app_factory()


@pytest.fixture
@pytest.mark.dependency(depends=["app"])
async def cli(aiohttp_client, app):
    return await aiohttp_client(app)


@pytest.fixture(scope="session")
async def db():
    load_dotenv()
    db = DBPool()
    db_url = os.getenv("DATABASE_URL", None)
    if not db_url:
        logger.error("[-] DATABASE_URL is not specified.")
        exit(1)
    await db.initialize(dsn=db_url)
    return db


@pytest.fixture(scope="module")
async def user_repo(db: DBPool):
    repo = UserRepository(db)
    return repo
