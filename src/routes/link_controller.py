from aiohttp import web

from src.repos.link_repo import LinkRepository


class LinkController:
    def register(self, app: web.Application):
        app.add_routes(
            [
                web.get("/api/v1/link", self.get_all_course),
            ]
        )

    def __init__(self, link: LinkRepository):
        self.link = link

    async def get_all_course(self, req: web.Request):
        pass
