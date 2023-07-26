from src.models.access_token import AccessToken
from src.repos.base_repo import DB
from src.service.database.dbpool import DBPool


class AccessTokenRepository(DB):
    def __init__(self, db: DBPool, access_token: AccessToken):
        super().__init__(db)
        self.access_token = access_token
