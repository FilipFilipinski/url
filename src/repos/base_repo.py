from src.service.database.dbpool import DBPool


class DB(object):
    def __init__(self, pool: DBPool):
        self.dbpool = pool

    def _call(func):
        async def wrapper(self, *args, **kwargs):
            async with self.dbpool.pool.acquire() as conn:
                return await func(self, conn, *args, **kwargs)

        return wrapper


def test_method(func):
    # marker annotation; methods marked with it _should never be called from non-test code_
    async def wrapper(self, *args, **kwargs):
        return await func(self, *args, **kwargs)

    return wrapper
