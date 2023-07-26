from aiohttp import web

from src.service.database.dbpool import DBPool


class HealthController:
    def register(self, app: web.Application):
        app.add_routes([web.get("/api/v1/health", self.get_health_status)])

    def __init__(self, db: DBPool):
        self.db = db

    async def get_health_status(self, _: web.Request):
        services = {"db": await self.db.check_connection()}

        status = all(services.items())
        return {
            "status": "healthy" if status else "unhealthy",
            "services": {k: "ok" if services[k] else "fail" for k in services},
        }, 200 if status else 503
