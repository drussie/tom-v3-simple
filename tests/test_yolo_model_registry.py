from __future__ import annotations

import hashlib
from argparse import Namespace
from collections.abc import Generator
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters import yolo_weights
from tom_v3_model_adapters.yolo_runtime import YoloRuntimeImportResult
from tom_v3_model_adapters.yolo_weights import (
    YoloClassMappingError,
    YoloWeightsValidationError,
    default_yolo_class_mapping,
    probe_yolo_model_metadata,
    validate_yolo_class_mapping,
    validate_yolo_weights,
)
from tom_v3_storage.db_models import Base, ModelRegistry, Observation, ProcessingRun

from apps.worker.cli import _handle_register_yolo_model
from apps.worker.services.yolo_model_registry import register_yolo_model


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )
    with session_factory() as session:
        yield session


def test_valid_weights_return_sha256_and_size(tmp_path: Path) -> None:
    root = tmp_path / "model_assets" / "yolo"
    weights = _write_weights(root, "fixture.pt", b"fake-yolo-weights")

    result = validate_yolo_weights(weights, allowed_roots=[root])

    assert result.status == "ok"
    assert result.size_bytes == len(b"fake-yolo-weights")
    assert result.sha256 == hashlib.sha256(b"fake-yolo-weights").hexdigest()
    assert result.sha256_matches is None


def test_missing_weights_fail_clearly(tmp_path: Path) -> None:
    root = tmp_path / "model_assets" / "yolo"

    with pytest.raises(YoloWeightsValidationError, match="does not exist") as exc_info:
        validate_yolo_weights(root / "missing.pt", allowed_roots=[root])

    assert exc_info.value.result.status == "missing"


def test_checksum_mismatch_fails_clearly(tmp_path: Path) -> None:
    root = tmp_path / "model_assets" / "yolo"
    weights = _write_weights(root, "fixture.pt", b"fake-yolo-weights")

    with pytest.raises(YoloWeightsValidationError, match="checksum mismatch") as exc_info:
        validate_yolo_weights(
            weights,
            allowed_roots=[root],
            required_sha256="0" * 64,
        )

    assert exc_info.value.result.status == "checksum_mismatch"
    assert exc_info.value.result.sha256_matches is False


def test_unsafe_weights_path_outside_allowed_root_fails(tmp_path: Path) -> None:
    allowed_root = tmp_path / "model_assets" / "yolo"
    outside_weights = _write_weights(tmp_path / "outside", "fixture.pt", b"outside")

    with pytest.raises(YoloWeightsValidationError, match="outside the allowed roots") as exc_info:
        validate_yolo_weights(outside_weights, allowed_roots=[allowed_root])

    assert exc_info.value.result.status == "invalid_path"


def test_unsupported_weight_suffix_fails(tmp_path: Path) -> None:
    root = tmp_path / "model_assets" / "yolo"
    weights = _write_weights(root, "fixture.txt", b"fake-yolo-weights")

    with pytest.raises(YoloWeightsValidationError, match="suffix is unsupported"):
        validate_yolo_weights(weights, allowed_roots=[root])


def test_default_class_mapping_validates() -> None:
    mapping = validate_yolo_class_mapping(default_yolo_class_mapping())

    assert mapping["ball"]["target_observation_type"] == "ball_detection"
    assert mapping["ball"]["target_label"] == "ball"
    assert mapping["player"]["target_observation_type"] == "player_detection"
    assert mapping["player"]["target_label"] == "player_unknown"


def test_invalid_target_observation_type_fails() -> None:
    with pytest.raises(YoloClassMappingError, match="target_observation_type"):
        validate_yolo_class_mapping(
            {
                "bad": {
                    "source_class_names": ["ball"],
                    "source_class_ids": [],
                    "target_observation_type": "tracklet",
                    "target_label": "ball",
                }
            }
        )


def test_invalid_target_label_fails() -> None:
    with pytest.raises(YoloClassMappingError, match="target_label"):
        validate_yolo_class_mapping(
            {
                "bad": {
                    "source_class_names": ["person"],
                    "source_class_ids": [],
                    "target_observation_type": "player_detection",
                    "target_label": "confirmed_player",
                }
            }
        )


def test_model_registry_row_created_from_valid_weights(
    db_session: Session,
    tmp_path: Path,
) -> None:
    root = tmp_path / "weights" / "yolo"
    weights = _write_weights(root, "fixture.pt", b"registry-weights")

    result = register_yolo_model(
        session=db_session,
        weights_path=str(weights),
        allowed_roots=[str(root)],
        model_name="pytest-yolo",
        model_version="test-v0",
    )

    assert result["ok"] is True
    assert result["status"] == "registered_created"
    model = db_session.get(ModelRegistry, result["model_registry_id"])
    assert model is not None
    assert model.model_family == "detection"
    assert model.metadata_jsonb["model_runtime"] == "ultralytics"
    assert model.metadata_jsonb["model_task"] == "detect"
    assert model.metadata_jsonb["weights_sha256"] == result["weights_sha256"]
    assert model.metadata_jsonb["weights_size_bytes"] == len(b"registry-weights")
    assert model.metadata_jsonb["class_map"]["ball"]["target_label"] == "ball"
    assert model.metadata_jsonb["milestone"] == "3B"
    assert db_session.scalar(select(func.count()).select_from(ProcessingRun)) == 0
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_repeated_registration_reuses_same_registry_row(
    db_session: Session,
    tmp_path: Path,
) -> None:
    root = tmp_path / "weights" / "yolo"
    weights = _write_weights(root, "fixture.pt", b"registry-weights")

    first = register_yolo_model(
        session=db_session,
        weights_path=str(weights),
        allowed_roots=[str(root)],
        model_name="pytest-yolo",
        model_version="test-v0",
    )
    second = register_yolo_model(
        session=db_session,
        weights_path=str(weights),
        allowed_roots=[str(root)],
        model_name="pytest-yolo",
        model_version="test-v0",
    )

    assert second["model_registry_id"] == first["model_registry_id"]
    assert second["status"] == "registered_reused"


def test_model_metadata_probe_skips_when_runtime_unavailable(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        yolo_weights,
        "try_import_yolo_runtime",
        lambda: YoloRuntimeImportResult(
            ultralytics=None,
            torch=None,
            cv2=None,
            missing_packages=("ultralytics",),
            import_errors={"ultralytics": "missing"},
        ),
    )

    metadata = probe_yolo_model_metadata(tmp_path / "fixture.pt")

    assert metadata["status"] == "unavailable"
    assert "ultralytics" in metadata["missing_packages"]


def test_model_metadata_probe_can_be_mocked(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fake_model = SimpleNamespace(names={0: "ball", 1: "person"}, task="detect")
    fake_ultralytics = SimpleNamespace(
        __version__="8.test",
        YOLO=lambda path: fake_model,
    )
    fake_torch = SimpleNamespace(__version__="2.test")

    monkeypatch.setattr(
        yolo_weights,
        "try_import_yolo_runtime",
        lambda: YoloRuntimeImportResult(
            ultralytics=fake_ultralytics,
            torch=fake_torch,
            cv2=None,
            missing_packages=(),
            import_errors={},
        ),
    )

    metadata = probe_yolo_model_metadata(tmp_path / "fixture.pt")

    assert metadata["status"] == "ok"
    assert metadata["task"] == "detect"
    assert metadata["class_names"] == ["ball", "person"]
    assert metadata["ultralytics_version"] == "8.test"
    assert metadata["torch_version"] == "2.test"


def test_worker_cli_handler_registers_model_from_temp_weights(
    db_session: Session,
    tmp_path: Path,
) -> None:
    root = tmp_path / "model_assets" / "yolo"
    weights = _write_weights(root, "worker.pt", b"worker-registry-weights")

    result = _handle_register_yolo_model(
        db_session,
        Namespace(
            weights_path=str(weights),
            model_name="worker-yolo",
            model_version="test-v0",
            required_sha256=None,
            allowed_roots=[str(root)],
            class_map_json=None,
            probe_model=False,
            device="cpu",
            created_by="pytest",
        ),
    )

    assert result["ok"] is True
    assert db_session.get(ModelRegistry, result["model_registry_id"]) is not None


def test_worker_cli_handler_does_not_create_model_for_invalid_weights(
    db_session: Session,
    tmp_path: Path,
) -> None:
    root = tmp_path / "model_assets" / "yolo"

    result = _handle_register_yolo_model(
        db_session,
        Namespace(
            weights_path=str(root / "missing.pt"),
            model_name="missing-yolo",
            model_version="test-v0",
            required_sha256=None,
            allowed_roots=[str(root)],
            class_map_json=None,
            probe_model=False,
            device="cpu",
            created_by="pytest",
        ),
    )

    assert result["ok"] is False
    assert result["status"] == "missing"
    assert db_session.scalar(select(func.count()).select_from(ModelRegistry)) == 0


def _write_weights(root: Path, file_name: str, data: bytes) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / file_name
    path.write_bytes(data)
    return path
