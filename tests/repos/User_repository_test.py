from datetime import datetime

from argon2 import PasswordHasher
from faker import Faker

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
