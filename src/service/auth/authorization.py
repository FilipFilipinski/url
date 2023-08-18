from uuid import UUID

from aiohttp import web
from aiohttp.web import HTTPUnauthorized
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.models.access_token import AccessToken
from src.models.user import User
from src.repos.token_repo import AccessTokenRepository
from src.repos.user_repo import UserRepository

ph = PasswordHasher()


class AuthorizationService:
    def __init__(self, user_repo: UserRepository, token_repo: AccessTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def login(self, email: str, password: str) -> AccessToken | None:
        """
        This method returns create a brand-new token
        that user can use to access API.

        Also, we should revoke any already generated
        tokens.

        Parameters:
          email (str): User's email
          password (str): User's password

        Returns:
          access_token (AccessToken): Authorization token
        """

        user = await self.user_repo.find(email=email)
        if not user:
            return None

        # Passwords doesn't match
        try:
            ph.verify(user.password, password)
        except VerifyMismatchError:
            return None

        token = await self.token_repo.generate(user.uid)
        return token

    async def register(self, username: str, password: str, email: str) -> AccessToken | None:
        """
        Creates a new user record
        and users token in the database.

        Parameters:
          username (str): User's username
          password (str): User's password
          email (str): User's email

        Returns:
          access_token (AccessToken): Authorization token
        """
        user = await self.user_repo.create(email=email, password=password, username=username)
        if not user:
            return None

        token = await self.token_repo.generate(user.uid)
        return token

    async def validate_token(self, token: UUID) -> bool:
        """
        This method validates given token based
        on database appearance of it.

        Parameters:
          token (UUID): Authorization token

        Returns:
          result (bool): Validation result
        """

        token = await self.token_repo.find(token)
        return bool(token)

    async def with_auth(self, req: web.Request) -> User:
        """
        Validates token that was sent in the request,
        if the token was valid, returns User.

        Throws HTTPUnauthorized in case if token isn't valid.

        Parameters:
          req (web.Request): AioHTTP's request object

        Returns:
          user (User): User object
        """

        auth_header = req.headers.get("Authorization", "")
        auth_segments = auth_header.split(" ")

        if len(auth_segments) != 2:
            raise HTTPUnauthorized()

        # If first segment isn't a Bearer typed, throw Unauthorized
        if auth_segments[0] != "Bearer":
            raise HTTPUnauthorized()

        try:
            token = UUID(auth_segments[1])
        except ValueError:
            raise HTTPUnauthorized()

        access_token = await self.token_repo.find(token)
        if not access_token:
            raise HTTPUnauthorized()

        return access_token.user
