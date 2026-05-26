from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import EvidenceArtifact, MediaAsset, Observation, ProcessingRun
from tom_v3_storage.local_media import calculate_sha256
from tom_v3_video.frame_extract import ExtractedFrame, extract_frame_image
from tom_v3_video.paths import local_path_from_uri_or_path

FRAME_ARTIFACT_TYPES = {"frame_image", "detection_frame_image"}
DETECTION_OBSERVATION_TYPES = {"ball_detection", "player_detection"}


class FrameArtifactExtractionError(ValueError):
    pass


def extract_frame_artifacts_for_run(
    session: Session,
    run_id: str,
    observation_id: str | None = None,
    observation_types: Iterable[str] | None = None,
    max_frames: int | None = None,
    output_root: str | Path = ".data/artifacts",
    image_format: str = "jpg",
    overwrite: bool = False,
    runner: Any | None = None,
) -> dict[str, Any]:
    run = session.get(ProcessingRun, run_id)
    if run is None:
        raise FrameArtifactExtractionError(f"processing run not found: {run_id}")
    media = session.get(MediaAsset, run.media_id)
    if media is None:
        raise FrameArtifactExtractionError(f"media asset not found: {run.media_id}")

    target_observations = _target_observations(
        session=session,
        run_id=run_id,
        observation_id=observation_id,
        observation_types=set(observation_types or DETECTION_OBSERVATION_TYPES),
    )
    frames = _limited_frames(target_observations, max_frames)
    source_path = _resolve_media_source_path(media)
    fps = _media_fps(media)
    output_root_path = Path(output_root).expanduser().resolve()

    artifact_ids: list[str] = []
    extracted_count = 0
    reused_count = 0
    skipped_count = 0
    frame_results: list[dict[str, Any]] = []
    observations_by_frame = _observations_by_frame(target_observations)

    for frame_number in frames:
        output_path = _frame_output_path(
            output_root_path=output_root_path,
            media_id=media.id,
            frame_number=frame_number,
            image_format=image_format,
        )
        existed_before = output_path.exists()
        extracted = extract_frame_image(
            source_path=source_path,
            frame_number=frame_number,
            fps=fps,
            output_path=output_path,
            image_format=image_format,
            overwrite=overwrite,
            runner=runner,
        )
        checksum = calculate_sha256(extracted.path)
        if existed_before and not overwrite:
            reused_count += 1
        else:
            extracted_count += 1

        frame_artifact = _get_or_create_artifact(
            session=session,
            media=media,
            run=run,
            extracted=extracted,
            checksum=checksum,
            source_path=source_path,
            artifact_type="frame_image",
            target_observation=None,
            overwrite=overwrite,
        )
        artifact_ids.append(frame_artifact.id)

        frame_observations = observations_by_frame.get(frame_number, [])
        if not frame_observations:
            skipped_count += 1
        for observation in frame_observations:
            targeted_artifact = _get_or_create_artifact(
                session=session,
                media=media,
                run=run,
                extracted=extracted,
                checksum=checksum,
                source_path=source_path,
                artifact_type="detection_frame_image",
                target_observation=observation,
                overwrite=overwrite,
            )
            artifact_ids.append(targeted_artifact.id)

        frame_results.append(
            {
                "frame_number": frame_number,
                "timestamp_ms": extracted.timestamp_ms,
                "uri": extracted.uri,
                "path": str(extracted.path),
                "checksum": checksum,
                "observation_ids": [observation.id for observation in frame_observations],
            }
        )

    session.commit()
    return {
        "run_id": run.id,
        "media_id": media.id,
        "extracted_count": extracted_count,
        "reused_count": reused_count,
        "skipped_count": skipped_count,
        "artifact_ids": sorted(set(artifact_ids)),
        "frames": frame_results,
        "output_root": str(output_root_path),
    }


def _target_observations(
    session: Session,
    run_id: str,
    observation_id: str | None,
    observation_types: set[str],
) -> list[Observation]:
    if observation_id is not None:
        observation = session.get(Observation, observation_id)
        if observation is None:
            raise FrameArtifactExtractionError(f"observation not found: {observation_id}")
        if observation.run_id != run_id:
            raise FrameArtifactExtractionError(
                f"observation {observation_id} does not belong to run {run_id}"
            )
        if observation.observation_type not in DETECTION_OBSERVATION_TYPES:
            raise FrameArtifactExtractionError(
                f"observation {observation_id} is not a detection observation"
            )
        return [observation]

    allowed_types = observation_types or DETECTION_OBSERVATION_TYPES
    unsupported = allowed_types - DETECTION_OBSERVATION_TYPES
    if unsupported:
        raise FrameArtifactExtractionError(
            f"unsupported observation_type for frame extraction: {', '.join(sorted(unsupported))}"
        )

    return list(
        session.scalars(
            select(Observation)
            .where(
                Observation.run_id == run_id,
                Observation.observation_family == "atomic",
                Observation.observation_type.in_(sorted(allowed_types)),
                Observation.frame_start.is_not(None),
            )
            .order_by(Observation.frame_start, Observation.observation_type, Observation.id)
        ).all()
    )


def _limited_frames(observations: list[Observation], max_frames: int | None) -> list[int]:
    frames = sorted(
        {
            observation.frame_start
            for observation in observations
            if observation.frame_start is not None
        }
    )
    if max_frames is not None:
        if max_frames < 0:
            raise FrameArtifactExtractionError("max_frames must be greater than or equal to 0")
        frames = frames[:max_frames]
    return frames


def _observations_by_frame(observations: list[Observation]) -> dict[int, list[Observation]]:
    grouped: dict[int, list[Observation]] = defaultdict(list)
    for observation in observations:
        if observation.frame_start is not None:
            grouped[observation.frame_start].append(observation)
    return dict(grouped)


def _resolve_media_source_path(media: MediaAsset) -> Path:
    candidate = (
        media.metadata_jsonb.get("stored_path")
        or media.metadata_jsonb.get("stored_uri")
        or media.source_uri
    )
    if not candidate:
        raise FrameArtifactExtractionError(f"media {media.id} has no local source path")
    path = local_path_from_uri_or_path(str(candidate))
    if not path.is_file():
        raise FrameArtifactExtractionError(f"media source file not found: {path}")
    return path


def _media_fps(media: MediaAsset) -> float:
    if media.fps is None or media.fps <= 0:
        raise FrameArtifactExtractionError(f"media {media.id} has no usable FPS")
    return media.fps


def _frame_output_path(
    output_root_path: Path,
    media_id: str,
    frame_number: int,
    image_format: str,
) -> Path:
    clean_format = image_format.lower().lstrip(".") or "jpg"
    return (
        output_root_path
        / "media"
        / media_id
        / "frames"
        / f"frame_{frame_number:08d}.{clean_format}"
    )


def _get_or_create_artifact(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    extracted: ExtractedFrame,
    checksum: str,
    source_path: Path,
    artifact_type: str,
    target_observation: Observation | None,
    overwrite: bool,
) -> EvidenceArtifact:
    existing = session.scalar(
        select(EvidenceArtifact).where(
            EvidenceArtifact.media_id == media.id,
            EvidenceArtifact.run_id == run.id,
            EvidenceArtifact.target_observation_id
            == (target_observation.id if target_observation is not None else None),
            EvidenceArtifact.artifact_type == artifact_type,
            EvidenceArtifact.frame_start == extracted.frame_number,
            EvidenceArtifact.uri == extracted.uri,
        )
    )
    if existing is not None and not overwrite:
        return existing

    artifact = EvidenceArtifact(
        media_id=media.id,
        run_id=run.id,
        target_observation_id=target_observation.id if target_observation is not None else None,
        artifact_type=artifact_type,
        uri=extracted.uri,
        frame_start=extracted.frame_number,
        frame_end=extracted.frame_number,
        timestamp_start_ms=extracted.timestamp_ms,
        timestamp_end_ms=extracted.timestamp_ms,
        checksum=checksum,
        metadata_jsonb={
            "frame_number": extracted.frame_number,
            "timestamp_ms": extracted.timestamp_ms,
            "frame_time_owner": "media_indexing",
            "extraction_method": extracted.extraction_method,
            "extraction_version": extracted.extraction_version,
            "source_media_uri": media.source_uri,
            "source_media_path": str(source_path),
            "output_path": str(extracted.path),
            "image_format": extracted.image_format,
            "placeholder": False,
            "shared_frame_artifact": target_observation is None,
        },
    )
    session.add(artifact)
    session.flush()
    return artifact
