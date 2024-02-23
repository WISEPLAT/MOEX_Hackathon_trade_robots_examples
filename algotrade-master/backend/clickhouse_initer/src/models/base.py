import orjson
from pydantic.generics import GenericModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JSONModel(GenericModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True
