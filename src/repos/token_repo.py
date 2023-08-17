from uuid import UUID

from asyncpg import Connection

from src.models.access_token import AccessToken
from src.repos.base_repo import DB
from src.repos.user_repo import UserRepository
from src.service.database.dbpool import DBPool


class AccessTokenRepository(DB):
    def __init__(self, db: DBPool, user_repo: UserRepository):
        super().__init__(db)
        self.user_repo = user_repo

    @DB._call
    async def generate(self, conn: Connection, uid: UUID) -> AccessToken | None:
        """
        Generates a new AccessToken object for given UserID.

        Parameters:
          uid (UUID): User's ID

        Returns:
          access_token (AccessToken): AccessToken object
        """

        user = await self.user_repo.find(uid=uid)
        if not user:
            return None

        await self.delete_all(uid)
        access_token = AccessToken(user=user)

        await conn.execute(
            """--sql
            INSERT INTO access_tokens(user_id, token, created_at)
            VALUES($1, $2, $3);
            """,
            uid,
            access_token.token,
            access_token.created_at,
        )

        return access_token

    @DB._call
    async def find(self, conn: Connection, token: UUID) -> AccessToken | None:
        """
        Returns AccessToken object with User relationship.

        Parameters:
          token (UUID): Authorization token

        Returns:
          access_token (AccessToken): AccessToken object
        """

        res = await conn.fetchrow(
            """--sql
            SELECT * FROM access_tokens
            WHERE token=$1 LIMIT 1;
            """,
            token,
        )

        if not res:
            return None

        # Finding a corresponding user to resolve our relation
        user = await self.user_repo.find(uid=res.get("user_id"))
        if not user:
            return None

        data = {
            "user": user,
        }
        data.update(res)

        return AccessToken.parse_obj(data)

    @DB._call
    async def delete_all(self, conn: Connection, uid: UUID):
        """
        Deletes all previous tokens from database where
        user_id equals to provided uid.

        Parameters:
          uid (UUID): User's ID
        """

        await conn.execute(
            """--sql
            DELETE FROM access_tokens WHERE user_id=$1;
            """,
            uid,
        )
