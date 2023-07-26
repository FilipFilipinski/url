from aiohttp import web

from src.repos.token_repo import AccessToken
from src.repos.user_repo import UserRepository


class AuthorizationService:
    def __init__(self, user_repo: UserRepository, token_repo: AccessToken):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def auth(self, req: web.Request) -> bool:
        """
        Validates token that was sent in the request,
        if the token was valid, returns True.
        Parameters:
          req (web.Request): AioHTTP's request object
        Returns:
         bool
        """

        auth_header = req.headers.get("Authorization", "")
        auth_segments = auth_header.split(" ")

        if len(auth_segments) != 2:
            return False

        # If first segment isn't a Bearer typed, throw Unauthorized
        if auth_segments[0] != "Bearer":
            return False

        try:
            token = str(auth_segments[1])
        except ValueError:
            return False

        access_token = await self.token_repo.find(token)
        if not access_token:
            return False

        return True
