from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from tom_v3_video.paths import local_path_from_uri_or_path


@dataclass(frozen=True)
class StoredMedia:
    path: Path
    uri: str


class LocalMediaStorage:
    def __init__(self, storage_root: str | Path = ".data/media") -> None:
        self.storage_root = Path(storage_root).expanduser().resolve()

    def store_file(
        self,
        source_path: str | Path,
        media_id: str,
        target_name: str | None = None,
    ) -> StoredMedia:
        source = resolve_media_file(source_path)
        media_dir = self.storage_root / media_id
        media_dir.mkdir(parents=True, exist_ok=True)
        destination = media_dir / (target_name or _default_target_name(source))
        shutil.copy2(source, destination)
        return StoredMedia(path=destination, uri=destination.resolve().as_uri())


def resolve_media_file(path_or_uri: str | Path) -> Path:
    path = local_path_from_uri_or_path(path_or_uri)
    if not path.is_file():
        raise FileNotFoundError(f"media file not found: {path}")
    return path


def calculate_sha256(path_or_uri: str | Path) -> str:
    path = resolve_media_file(path_or_uri)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _default_target_name(source: Path) -> str:
    return f"original{source.suffix.lower()}"
