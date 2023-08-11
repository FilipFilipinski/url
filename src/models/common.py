import json

from pydantic import BaseModel


def plain_dict(entity: BaseModel) -> dict[str, any]:
    """
    Convert a pydantic entity to a (possibly nested) dict involving only strings. If slow (test it!),
    consider using https://github.com/ijl/orjson orjson.loads(...).

    Note,
    .dict() would give
    {
        'uid': UUID('063a815b-d35c-4ea5-9445-5658671660db'),
        'sub': {'dt': datetime.date(2012, 1, 18), 'a': 12}
    }
    # functionality is perhaps coming to pydantic,
    # https://stackoverflow.com/questions/65622045/pydantic-convert-to-jsonable-dict-not-full-json-string

    :param entity:
    :return: dict[str,str | dict]
    """
    return json.loads(entity.json())
