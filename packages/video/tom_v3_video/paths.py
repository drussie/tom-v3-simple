from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname


def local_path_from_uri_or_path(path_or_uri: str | Path) -> Path:
    value = str(path_or_uri)
    if value.startswith("file://"):
        parsed = urlparse(value)
        return Path(url2pathname(parsed.path)).expanduser().resolve()
    return Path(value).expanduser().resolve()
