import random
import string
from uuid import UUID

from argon2 import PasswordHasher
from asyncpg import Connection

from src.models.link import Link
from src.repos.base_repo import DB

ph = PasswordHasher()


def random_link():
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join([random.choice(chars) for _ in range(6)])


class LinkRepository(DB):
    async def create(self, user_uuid: UUID, link: str, proposed_name: str = None, password: str = None) -> Link | None:
        """
        Creates a new record in url table.

        Parameters:
          user_uuid (UUID),
          link (str),
          proposed_name (str),
          password (str),
        Returns:
          Link: Link's object
        """
        if proposed_name:
            link = await self.find(proposed_name=proposed_name)

            if link:
                return None
        else:
            while True:
                proposed_name = random_link()
                if not await self.find(proposed_name=proposed_name):
                    break

        protected = False

        if password:
            protected = True
            password = ph.hash(str(password))

        link = Link(
            owner_uid=user_uuid,
            original_link=link,
            short_link=proposed_name,
            protected=protected,
            password=password if password else None,
        )
        return await self.save(link)

    @DB._call
    async def find(
        self, conn: Connection, proposed_name: str = None, link_uid: UUID = None, user_uuid: UUID = None
    ) -> Link | None:
        """
        Returns User object (if exists with given email or id).

        Parameters:
          proposed_name (str|Optional): proposed_name
          link_uid (UUID|Optional): Link uid
          user_uuid (UUID|Optional): User uid

        Returns:
          link (Link | None): Links's object or None
        """

        if proposed_name or link_uid or user_uuid:
            u = await conn.fetchrow(
                """--sql
                SELECT * FROM links
                WHERE l_uid=$1 OR owner_id=$2 OR short_link=$3;
                """,
                link_uid,
                user_uuid,
                proposed_name,
            )

            if u:
                response = [Link.parse_obj(link) for link in u]
                return response if len(response) > 1 else response[0]
        return None

    @DB._call
    async def save(self, conn: Connection, link: Link) -> Link:
        """
        If Link class got l_uid parameter functions change link data else
        function creat new link.

        Parameters:
          link (Link)

        Returns:
          link (Link)
        """
        if link.l_uid:
            returned_link = await conn.fetchrow(
                """--sql
                UPDATE links
                SET original_link=$1, short_link=$2, protected=$3, password=$4
                WHERE id=$5
                RETURNING *;
                """,
                link.original_link,
                link.short_link,
                link.protected,
                link.password,
            )
        else:
            returned_link = await conn.fetchrow(
                """--sql
                INSERT INTO users(owner_uid, original_link, short_link, protected, password, created_at)
                VALUES($1, $2, $3, $4, $5, $6)
                RETURNING *;
                """,
                link.owner_uid,
                link.original_link,
                link.short_link,
                link.protected,
                link.password,
                link.created_at,
            )
        return Link.parse_obj(returned_link)
