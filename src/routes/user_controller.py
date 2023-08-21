from json import JSONDecodeError

from aiohttp import web
from aiohttp.web import (HTTPBadRequest, HTTPConflict, HTTPForbidden,
                         HTTPNotAcceptable, HTTPNotFound)

from src.helpers.uid_from_link import get_uid
from src.repos.user_repo import UserRepository
from src.service.auth.authorization import AuthorizationService


class UserController:
    def register(self, app: web.Application):
        app.add_routes(
            [
                web.get("/api/v1/me", self.get_user_info),
                web.post("/api/v1/login", self.login_user),
                web.get("/api/v1/user", self.all_users),
                web.post("/api/v1/user", self.create_user),
                web.get("/api/v1/user/{user_uid}", self.get_user),
                web.delete("/api/v1/user/{user_uid}", self.delete_user),
                web.put("/api/v1/user/{user_uid}", self.change_admin),
            ]
        )

    def __init__(
        self,
        user: UserRepository,
        auth: AuthorizationService,
    ):
        self.user = user
        self.auth = auth

    async def get_user_info(self, req: web.Request):
        # With authentication guard
        user = await self.auth.with_auth(req)
        return user

    async def all_users(self, req: web.Request):
        try:
            page = int(req.query.get("page", "1"))
            per_page = int(req.query.get("per_page", "10"))
        except ValueError:
            page = 1
            per_page = 10

        phrase = req.query.get("phrase", "")

        if (await self.auth.with_auth(req)).admin:
            return {
                "users": await self.user.search(phrase, page, per_page),
                "extras": {
                    "next_page_exists": await self.user.next_page_exists(phrase, page, per_page),
                    "page": page,
                    "per_page": per_page,
                },
            }, 200

        raise HTTPForbidden(reason="Access denied")

    async def login_user(self, req: web.Request):
        try:
            params = await req.json()
        except JSONDecodeError:
            raise HTTPBadRequest(reason="Provided JSON data isn't a valid JSON.")

        email, password = params.get("email"), params.get("password")

        token = await self.auth.login(email, password)
        if not token:
            raise HTTPNotAcceptable(reason="Invalid username or password.")

        return token

    async def create_user(self, req: web.Request):
        try:
            params = await req.json()
        except JSONDecodeError:
            raise HTTPBadRequest(reason="Provided JSON data isn't a valid JSON.")

        password = params.get("password")
        username = params.get("username")
        email = params.get("email")

        # TODO sending an email to verify that the email is definitely correct
        token = await self.auth.register(username, password, email)
        if not token:
            raise HTTPConflict(reason="This username is already taken.")

        return token, 201

    # Admin panel

    async def delete_user(self, req: web.Request):
        user = await self.auth.with_auth(req)
        user_uid = await get_uid(req, "user_uid")

        # Only admin and user can remove account
        if user.admin or user.uid == user_uid:

            if await self.user.find(uid=user_uid):
                if await self.user.delete(uid=user_uid):
                    return {"message": "User was successfully removed"}, 200

            raise HTTPNotFound(reason="Username does not exists.")
        raise HTTPForbidden(reason="Access denied")

    async def get_user(self, req: web.Request):
        if await self.auth.with_auth(req):
            user = await self.user.find(uid=await get_uid(req, "user_uid"))
            if user:
                return user
            return None
        raise HTTPForbidden(reason="Access denied")

    async def change_admin(self, req: web.Request):
        user_uid = await get_uid(req, "user_uid")

        if (await self.auth.with_auth(req)).admin:
            return await self.user.change_admin_status(uid=user_uid)
        raise HTTPForbidden(reason="Access denied")
