from __future__ import annotations

import json
import os
import sys
from typing import Any

from sqlalchemy.orm import sessionmaker
from tom_v3_observations.synthetic import create_synthetic_run, verify_synthetic_run
from tom_v3_storage.db_models import Base

from apps.api.db import build_engine
from apps.api.routers.viewer import build_viewer_run_payload

DEFAULT_DATABASE_URL = "sqlite+pysqlite:///./tmp_tom_v3_smoke.db"


def run_smoke(database_url: str | None = None) -> dict[str, Any]:
    engine = build_engine(database_url or os.getenv("TOM_V3_DATABASE_URL", DEFAULT_DATABASE_URL))
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )

    with session_factory() as session:
        seed_result = create_synthetic_run(session)
        run_id = str(seed_result["run_id"])
        verification = verify_synthetic_run(session, run_id)
        viewer_payload = build_viewer_run_payload(session, run_id)

    checks = _check_viewer_payload(viewer_payload)
    checks["synthetic_verifier"] = bool(verification["ok"])
    ok = all(checks.values())
    return {
        "ok": ok,
        "run_id": run_id,
        "checks": checks,
        "verification": verification,
    }


def _check_viewer_payload(viewer_payload: dict[str, Any] | None) -> dict[str, bool]:
    if viewer_payload is None:
        return {
            "viewer_payload": False,
            "gameplay_state": False,
            "non_gameplay_state": False,
            "uncertain_state": False,
            "ball_track": False,
            "near_player_track": False,
            "far_player_track": False,
            "homography_placeholder": False,
            "bounce_candidate": False,
            "tracking_gap_candidate": False,
            "hit_candidate": False,
            "lineage": False,
            "artifacts": False,
        }

    observations = viewer_payload["observations"]
    tracklets = viewer_payload["tracklets"]
    observation_types = {row["observation_type"] for row in observations}
    view_states = {
        row["gameplay"]["view_state"]
        for row in observations
        if row.get("gameplay") is not None
    }
    track_rows = {
        str(tracklet["metadata_jsonb"].get("viewer_row"))
        for tracklet in tracklets
        if tracklet.get("metadata_jsonb")
    }
    coverage_states = {
        segment["state"]
        for tracklet in tracklets
        for segment in tracklet["metadata_jsonb"].get("coverage_segments", [])
    }

    return {
        "viewer_payload": True,
        "gameplay_state": "gameplay" in view_states,
        "non_gameplay_state": "non_gameplay" in view_states,
        "uncertain_state": "uncertain" in view_states,
        "ball_track": "Ball track" in track_rows,
        "near_player_track": "Near player" in track_rows,
        "far_player_track": "Far player" in track_rows,
        "track_gap": "gap" in coverage_states,
        "low_confidence": "low_confidence" in coverage_states,
        "homography_placeholder": "homography_placeholder" in observation_types,
        "bounce_candidate": "bounce_candidate" in observation_types,
        "tracking_gap_candidate": "tracking_gap_candidate" in observation_types,
        "hit_candidate": "hit_candidate" in observation_types,
        "lineage": len(viewer_payload["lineage"]) > 0,
        "artifacts": len(viewer_payload["artifacts"]) > 0,
    }


def main() -> int:
    result = run_smoke()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
