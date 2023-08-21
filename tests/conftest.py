import asyncio
import os

import pytest
from argon2 import PasswordHasher
from dotenv import load_dotenv
from faker import Faker
from loguru import logger

from src.app import async_app_factory
from src.repos.token_repo import AccessTokenRepository
from src.repos.user_repo import UserRepository
from src.service.auth.authorization import AuthorizationService
from src.service.database.dbpool import DBPool

faker = Faker()
ph = PasswordHasher()


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


@pytest.fixture(scope="module")
async def token_repo(db: DBPool, user_repo: UserRepository):
    token_repo = AccessTokenRepository(db, user_repo)
    return token_repo


@pytest.fixture(scope="module")
async def auth(db: DBPool, user_repo: UserRepository, token_repo: AccessTokenRepository):
    auth = AuthorizationService(user_repo, token_repo)
    return auth


@pytest.fixture(scope="function", autouse=True)
async def example_user(user_repo: UserRepository):
    username = str(faker.first_name())
    email = faker.email()
    password = "random"
    user = await user_repo.create(email=email, password=password, username=username)
    yield user
    await user_repo.delete(uid=user.uid)


@pytest.fixture(scope="function", autouse=True)
async def example_user_admin(user_repo: UserRepository):
    username = str(faker.first_name()) + "admin"
    email = faker.email() + ".admin"
    password = "random"
    user = await user_repo.create(email=email, password=password, username=username)
    await user_repo.change_admin_status(uid=user.uid)
    yield await user_repo.find(uid=user.uid)
    await user_repo.delete(uid=user.uid)
