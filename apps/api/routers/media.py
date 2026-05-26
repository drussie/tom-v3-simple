from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.media import MediaAssetCreate, MediaAssetRead, MediaRegisterFileRequest
from tom_v3_storage.db_models import MediaAsset
from tom_v3_storage.media_indexer import MediaIndexingError, index_media_file

from apps.api.db import get_session

router = APIRouter(tags=["media"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/media", response_model=MediaAssetRead, status_code=status.HTTP_201_CREATED)
def create_media(request: MediaAssetCreate, session: SessionDep) -> MediaAsset:
    media = MediaAsset(**request.model_dump())
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


@router.post(
    "/media/register-file",
    response_model=MediaAssetRead,
    status_code=status.HTTP_201_CREATED,
)
def register_media_file(request: MediaRegisterFileRequest, session: SessionDep) -> MediaAsset:
    try:
        return index_media_file(
            session=session,
            source_path=request.source_path,
            copy_to_storage=request.copy_to_storage,
            media_name=request.media_name,
            storage_root=request.storage_root,
        )
    except MediaIndexingError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/media/{media_id}", response_model=MediaAssetRead)
def get_media(media_id: str, session: SessionDep) -> MediaAsset:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="media asset not found")
    return media
