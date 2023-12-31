import os

import aiohttp_cors
from dotenv import load_dotenv
from loguru import logger


class Context:
    context: "Context"  # singleton reference for dumb frameworks without mechanisms of dependency injection

    def __init__(self):
        # if at all - just place uninitialized classes here
        # local imports to avoid circular dependencies (services might want to import Context
        from aiohttp import web

        from src.repos.link_repo import LinkRepository
        from src.repos.stat_repo import StatRepository
        from src.repos.token_repo import AccessTokenRepository
        from src.repos.user_repo import UserRepository
        from src.routes.health_controller import HealthController
        from src.routes.link_controller import LinkController
        from src.routes.user_controller import UserController
        from src.service.auth.authorization import AuthorizationService
        from src.service.database.dbpool import DBPool

        Context.context = self
        self.db = DBPool()
        # app
        self.app = web.Application()

        # services
        self.user_repo = UserRepository(self.db)
        self.link_repo = LinkRepository(self.db)
        self.stat_repo = StatRepository(self.db)
        self.token_repo = AccessTokenRepository(self.db, self.user_repo)

        self.auth = AuthorizationService(self.user_repo, self.token_repo)

        # controllers
        self.controllers = [
            HealthController(self.db),
            LinkController(self.link_repo),
            UserController(self.user_repo, self.auth),
        ]

    async def initialize(self):
        load_dotenv()
        # async logic for initialization of all resources, in proper order
        await self.initialize_db()
        await self.initialize_app()

    async def shutdown(self):
        logger.warning("app going down; disabling components!")
        # proper order of the shutdown procedure

    async def initialize_app(self):
        from src.helpers.middlewares import setup_middlewares

        # controllers should be set up in dedicated method, and put into a list, for possible further processing
        for controller in self.controllers:
            controller.register(self.app)

        await setup_middlewares(self.app)

        cors = aiohttp_cors.setup(
            self.app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
            },
        )

        for route in list(self.app.router.routes()):
            cors.add(route)

    async def initialize_db(self):
        db_url = os.getenv("DATABASE_URL", None)
        if not db_url:
            logger.error("[-] DATABASE_URL is not specified.")
            exit(1)
        await self.db.initialize(dsn=db_url)
