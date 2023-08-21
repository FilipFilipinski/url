from json import dumps

from aiohttp.test_utils import TestClient
from faker import Faker

from src.models.user import User
from src.repos.token_repo import AccessTokenRepository
from src.repos.user_repo import UserRepository
from src.service.auth.authorization import AuthorizationService
from tests.common import random_string

fake = Faker()


async def test_if_healthy(cli: TestClient, user_repo: UserRepository):
    user_data = {"username": f"{fake.name()}", "email": f"f{fake.email()}", "password": f"{random_string()}"}
    resp = await cli.post(
        "/api/v1/user",
        data=dumps(user_data, default=str),
    )

    assert resp.status == 201
    user_data_returned = (await resp.json()).get("user")
    assert user_data_returned.get("username") == user_data.get("username")
    assert user_data_returned.get("email") == user_data.get("email")


async def test_change_user_admin_status(
    cli: TestClient,
    user_repo: UserRepository,
    example_user_admin: User,
    example_user: User,
    auth: AuthorizationService,
    token_repo: AccessTokenRepository,
):
    data = await auth.login(example_user_admin.email, "random")
    assert example_user_admin.admin is True

    assert example_user.admin is False
    uid = example_user.uid

    await cli.put(
        f"/api/v1/user/{str(uid)}",
        headers={"Authorization": f"Bearer {str(data.token)}"},
    )
    assert (await user_repo.find(uid=uid)).admin is True


async def test_remove_user_by_admin(
    cli: TestClient,
    user_repo: UserRepository,
    example_user_admin: User,
    example_user: User,
    auth: AuthorizationService,
    token_repo: AccessTokenRepository,
):
    data = await auth.login(example_user_admin.email, "random")
    assert example_user_admin.admin is True

    assert example_user.admin is False
    uid = example_user.uid

    res = await cli.delete(
        f"/api/v1/user/{str(uid)}",
        headers={"Authorization": f"Bearer {str(data.token)}"},
    )
    assert res.status == 200
    assert await user_repo.find(uid=uid) is None


async def test_remove_user_by_user(
    cli: TestClient,
    user_repo: UserRepository,
    example_user_admin: User,
    example_user: User,
    auth: AuthorizationService,
    token_repo: AccessTokenRepository,
):
    data = await auth.login(example_user.email, "random")

    uid = example_user.uid

    res = await cli.delete(
        f"/api/v1/user/{str(uid)}",
        headers={"Authorization": f"Bearer {str(data.token)}"},
    )
    assert res.status == 200
    assert await user_repo.find(uid=uid) is None


async def test_other_user_can_not_delete_user(
    cli: TestClient,
    user_repo: UserRepository,
    example_user_admin: User,
    example_user: User,
    auth: AuthorizationService,
    token_repo: AccessTokenRepository,
):
    data = await auth.login(example_user.email, "random")

    uid = example_user.uid

    res = await cli.delete(
        f"/api/v1/user/{str(uid)}",
        headers={"Authorization": f"Bearer {str(data.token)[:-4]+'hehe'}"},
    )
    assert res.status == 401
    assert await user_repo.find(uid=uid) is not None
