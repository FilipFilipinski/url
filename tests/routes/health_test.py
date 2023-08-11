from aiohttp.test_utils import TestClient


async def test_if_healthy(cli: TestClient):
    resp = await cli.get("/api/v1/health")

    assert resp.status == 200
    assert (await resp.json()).get("status") == "healthy"


async def test_all_services_healthy(cli: TestClient):
    resp = await cli.get("/api/v1/health")

    services = (await resp.json()).get("services")
    statuses = [x == "ok" for x in services.values()]

    assert resp.status == 200
    assert all(statuses)
