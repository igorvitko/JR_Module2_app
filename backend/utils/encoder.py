import json
import contextlib
from datetime import datetime
from urllib.parse import urlparse, parse_qs


class AppJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def parser_url(url) -> tuple[str, dict[str, str]]:
    parsed_url = urlparse(url)
    path = parsed_url.path
    params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
    return path, params


# test
# url = "http://localhost/api/images?tab=images&page=1&limit=10&order=desc"
url = "http://localhost/api/images/imagesss.png"
print(parser_url(url))