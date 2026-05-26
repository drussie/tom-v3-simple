from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base, Observation, ProcessingRun

from apps.worker.cli import _handle_smoke_real_yolo_local
from apps.worker.services.real_yolo_smoke import (
    build_real_yolo_smoke_plan,
    run_real_yolo_local_smoke,
)


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


def runtime_ok(**kwargs):
    return {
        "status": "ok",
        "requested_device": kwargs.get("requested_device", "cpu"),
        "resolved_device": "cpu",
        "ultralytics_available": True,
        "torch_available": True,
        "opencv_available": True,
        "missing_packages": [],
    }


def runtime_missing(**kwargs):
    return {
        "status": "unavailable",
        "requested_device": kwargs.get("requested_device", "cpu"),
        "resolved_device": "cpu",
        "ultralytics_available": False,
        "torch_available": False,
        "opencv_available": False,
        "missing_packages": ["ultralytics", "torch", "opencv-python-headless"],
        "install_hint": "install optional YOLO runtime",
    }


def test_smoke_plan_builder_creates_expected_yolo_steps() -> None:
    plan = build_real_yolo_smoke_plan(
        source_path="/tmp/sample.mp4",
        weights_path="model_assets/yolo/local.pt",
        model_name="local-yolo-smoke",
        model_version="local-v0",
        device="cpu",
        run_tracklets=True,
    )

    command_text = "\n".join(plan["commands"])
    assert "yolo-runtime-probe --device cpu" in command_text
    assert "register-yolo-model" in command_text
    assert "--weights-path model_assets/yolo/local.pt" in command_text
    assert "index-media --source-path /tmp/sample.mp4" in command_text
    assert "run-detection-adapter" in command_text
    assert "--adapter yolo" in command_text
    assert "--model-registry-id <model_registry_id>" in command_text
    assert "extract-frame-artifacts" in command_text
    assert "build-tracklets" in command_text
    assert "--adapter fixture" not in command_text
    assert plan["warnings"]["observation_only"] is True
    assert plan["warnings"]["no_adjudication"] is True
    assert plan["warnings"]["no_fixture_fallback"] is True


def test_smoke_plan_only_does_not_require_runtime_or_assets(db_session: Session) -> None:
    result = run_real_yolo_local_smoke(
        session=db_session,
        source_path=None,
        weights_path=None,
        plan_only=True,
    )

    assert result["status"] == "planned"
    assert result["ok"] is True
    assert result["warnings"]["observation_only"] is True


def test_missing_runtime_returns_structured_skip_without_fixture_fallback(
    db_session: Session,
) -> None:
    result = run_real_yolo_local_smoke(
        session=db_session,
        source_path="/tmp/sample.mp4",
        weights_path="model_assets/yolo/local.pt",
        probe_runtime=runtime_missing,
    )
    observation_count = db_session.scalar(select(func.count()).select_from(Observation))

    assert result["status"] == "skipped"
    assert result["skip_reason"] == "yolo_runtime_unavailable"
    assert result["ok"] is True
    assert result["warnings"]["no_fixture_fallback"] is True
    assert observation_count == 0


def test_missing_weights_returns_structured_skip(db_session: Session, tmp_path: Path) -> None:
    source = tmp_path / "sample.mp4"
    source.write_bytes(b"not-used-with-missing-weights")
    result = run_real_yolo_local_smoke(
        session=db_session,
        source_path=str(source),
        weights_path=str(tmp_path / "weights" / "missing.pt"),
        probe_runtime=runtime_ok,
    )
    run_count = db_session.scalar(select(func.count()).select_from(ProcessingRun))

    assert result["status"] == "skipped"
    assert result["skip_reason"] == "missing_weights"
    assert result["ok"] is True
    assert run_count == 0


def test_cli_handler_supports_plan_only_smoke(db_session: Session) -> None:
    result = _handle_smoke_real_yolo_local(
        db_session,
        Namespace(
            source_path=None,
            weights_path=None,
            model_name="local-yolo-smoke",
            model_version="local-v0",
            device="cpu",
            frame_sample_rate=30,
            max_frames=3,
            output_root=".data/artifacts",
            allowed_roots=None,
            copy_to_storage=True,
            run_tracklets=False,
            output_debug_artifact=True,
            plan_only=True,
        ),
    )

    assert result["status"] == "planned"
    assert "--model-registry-id <model_registry_id>" in "\n".join(result["plan"]["commands"])


def test_docs_reference_model_registry_id_for_real_yolo_smoke() -> None:
    docs = "\n".join(
        [
            Path("docs/model_adapters/yolo_real_runtime_smoke_v0.md").read_text(),
            Path("docs/dev/local_demo_runbook.md").read_text(),
        ]
    )

    assert "smoke-real-yolo-local" in docs
    assert "--model-registry-id <model_registry_id>" in docs
    assert "--adapter yolo" in docs
