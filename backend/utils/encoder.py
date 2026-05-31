import json
from datetime import datetime
import contextlib


class AppJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def get_query_params(path) -> dict[str, str]:
    if "?" not in path:
        return {}

    query = path.split("?")[1]
    params = {}

    for pair in query.split("&"):
        with contextlib.suppress(AttributeError):
            key, value = pair.split("=", 1)
            params[key] = value

    return params
