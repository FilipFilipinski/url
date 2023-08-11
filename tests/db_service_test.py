import pytest

from src.service.database.dbpool import DBPool


@pytest.mark.asyncio
async def test_db_healthy(db: DBPool):
    db_connection_ok = await db.check_connection()
    assert db_connection_ok
