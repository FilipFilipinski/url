from datetime import datetime

from argon2 import PasswordHasher
from faker import Faker

from src.models.user import User
from src.repos.user_repo import UserRepository
from tests.common import random_string

faker = Faker()
ph = PasswordHasher()


async def test_can_create_user(user_repo: UserRepository):
    username = str(faker.first_name())
    email = faker.email()
    password = random_string()

    user = await user_repo.create(email=email, password=password, username=username)

    assert user.uid is not None

    assert user.email == email
    assert ph.verify(user.password, password)
    assert user.username == username

    assert int(user.date.timestamp()) <= int(datetime.now().timestamp())

    await user_repo.delete(uid=user.uid)

    assert await user_repo.find(uid=user.uid) is None


async def test_can_change_admin(user_repo: UserRepository, example_user: User):
    assert example_user.admin is False

    await user_repo.change_admin_status(example_user.uid)
    assert (await user_repo.find(uid=example_user.uid)).admin is True

    await user_repo.change_admin_status(example_user.uid)
    assert (await user_repo.find(uid=example_user.uid)).admin is False
