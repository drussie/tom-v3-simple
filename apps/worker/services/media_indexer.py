from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_storage.db_models import MediaAsset
from tom_v3_storage.media_indexer import index_media_file


def index_media(
    session: Session,
    source_path: str | Path,
    copy_to_storage: bool = True,
    media_name: str | None = None,
    storage_root: str | Path = ".data/media",
    probe_runner: Any | None = None,
) -> MediaAsset:
    return index_media_file(
        session=session,
        source_path=source_path,
        copy_to_storage=copy_to_storage,
        media_name=media_name,
        storage_root=storage_root,
        probe_runner=probe_runner,
    )
