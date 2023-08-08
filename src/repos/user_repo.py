from datetime import datetime
from uuid import UUID

from argon2 import PasswordHasher
from asyncpg import Connection

from src.models.user import User
from src.repos.base_repo import DB

ph = PasswordHasher()


class UserRepository(DB):

    async def create(self, email: str, password: str, username: str) -> User | None:
        """
        Creates a new record in users table.

        Parameters:
          email (str),
          password (str),
          username (str),
        Returns:
          user (User): User's object
        """

        # Ensure that we won't be overwriting existing user
        user = await self.find(email=email)
        if user:
            return None

        if password:
            # Hash given password using argon2
            password = ph.hash(str(password))

        user = User(email=email, password=password, username=username, date=datetime.now())
        return await self.save(user)

    @DB._call
    async def find(self, conn: Connection, email: str = None, uid: UUID = None) -> User | None:
        """
        Returns User object (if exists with given email or id).

        Parameters:
          email (int|Optional): User's phone
          uid (int|Optional): User uid

        Returns:
          user (User | None): User's object or None
        """

        if email or id:
            u = await conn.fetchrow(
                """--sql
                SELECT * FROM users
                WHERE email=$1 OR uid=$2;
                """,
                email,
                uid,
            )

            if u:
                return User.parse_obj(u)
        return None

    @DB._call
    async def delete(self, conn: Connection, uid: UUID = None) -> bool:
        """
        Deletes a User record from database.

        Parameters:
          uid (UUID): User's uid

        Returns:
          result (bool): True if User was deleted successfully else False
        """

        if not await self.find(uid=uid):
            return False

        await conn.fetchval(
            """--sql
            DELETE FROM users
            WHERE uid=$1;
            """,
            uid,
        )

        return True

    @DB._call
    async def save(self, conn: Connection, user: User) -> User:
        """
        If User class got id parameter functions change user data else
        function creat new user.

        Parameters:
          user (User)

        Returns:
          user (User)
        """
        if user.uid:
            u = await conn.fetchrow(
                """--sql
                UPDATE users
                SET email=$1, password=$2, username=$3
                WHERE id=$5
                RETURNING *;
                """,
                user.email,
                user.password,
                user.username,
            )
        else:
            u = await conn.fetchrow(
                """--sql
                INSERT INTO users(email, password, username, created_at)
                VALUES($1, $2, $3, $4)
                RETURNING *;
                """,
                user.email,
                user.password,
                user.username,
                user.date
            )
        return User.parse_obj(u)
