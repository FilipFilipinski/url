from json import JSONDecodeError
from uuid import UUID

from aiohttp.web import HTTPBadRequest


async def get_uid(req, name: str, version: int = 4) -> UUID:
    try:
        searched_id = str(req.match_info.get(name))
        uuid_obj = UUID(searched_id, version=version)
        if str(uuid_obj) == searched_id:
            return uuid_obj
    except (JSONDecodeError, ValueError):
        raise HTTPBadRequest(reason=f"Provided {name} data isn't a valid.")
