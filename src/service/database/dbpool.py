from time import sleep

import asyncpg
from loguru import logger


class DBPool:
    pool: asyncpg.Pool

    async def initialize(self, dsn: str):
        logger.info("Initializing database pool...")
        try:
            self.pool = await asyncpg.create_pool(dsn, timeout=30, command_timeout=5)
        except (TimeoutError, ConnectionRefusedError):
            logger.error("Couldn't connect to database...")
            logger.error("Please check if provided data is valid.")

            # when running in gunicorn context, for every exited worker,
            # gunicorn will respawn that worker, which results in
            # loop using 1 whole cpu core ;/
            # it's good to wait some time before retrying to connect to
            # database again, to avoid such cpu usage
            sleep(2.5)
            exit(1)

    async def check_connection(self) -> bool:
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("SELECT 1")
        except ConnectionRefusedError:
            return False

        return True
