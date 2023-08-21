import asyncio
import traceback
from datetime import datetime
from json import JSONEncoder

from aiohttp import web
from loguru import logger
from pydantic import BaseModel, ValidationError

from src.models.common import plain_dict


class NestedSerializer(JSONEncoder):
    def default(self, o) -> dict:
        if isinstance(o, BaseModel):
            return plain_dict(o)

        # datetime.__str__ somehow returns string that
        # doesn't comply with ISO 8601 (there's a "T" missing)
        # in between of date and time section.
        if isinstance(o, datetime):
            return o.isoformat()

        if hasattr(o, "__dict__"):
            return o.__dict__

        return str(o)


@web.middleware
async def jsonify_middleware(request, handler):
    """
    Automatic version to serialize responses to web.json_response
    - if already a web.Response -- just forward it
    - if a pure tuple -- split in two (special case???)
    - if something else (e.g. pydantic model object, or lists of such) -- use NestedSerializer, calling
       .to_dict() if possible, or using pydantic way to serialize nested objects to proper json's.
    """
    try:
        res = await handler(request)
        if isinstance(res, web.Response):
            return res
        elif isinstance(res, tuple):
            # when do we need this?? (can be tricky if somebody accidentally sends a tuple instead of a list)
            # ok -- so idea is to use this with (response,stats); why hot have custom HttpResponse(response,status)?
            return web.json_response(res[0], dumps=NestedSerializer().encode, status=res[1])
        elif asyncio.iscoroutine(res):
            logger.warning(
                "You probably wanted to return a value, but we've received as Coroutine instead. "
                f"You might want to add `await` before the returning function call. (func: {handler.__name__})"
            )
            pass

        return web.json_response(res, dumps=NestedSerializer().encode)

    except web.HTTPException as ex:
        return web.json_response(
            {
                "status": ex.status,
                "message": str(ex),
            },
            status=ex.status,
        )
    except ValidationError as ex:
        return web.json_response(
            {
                "status": 400,
                "message": "Invalid data provided",
                "errors": {e["loc"][0]: e["msg"] for e in ex.errors()},
            },
            status=400,
        )

    except TimeoutError:
        # throw ServiceUnavailable on TimeoutError
        return web.json_response({"status": 503, "message": "Request timed out."}, status=503)

    except Exception as ex:
        # throw 500 on any other error
        msg = str(ex) or "No message was provided."
        logger.error(f"{request.path} | {type(ex).__name__}: {msg}")
        traceback.print_exc()

        return web.json_response({"status": 500, "message": "Internal Server Error"}, status=500)
