from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.tom_v3_expansion_completion_freeze import (
    CURRENT_MAIN_COMMIT,
    FORBIDDEN_FREEZE_CLAIMS,
    FROZEN_CONTRACT_REFS,
    PROTECTED_SAMPLE_POINT_IDS,
    TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE,
    TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION,
    TOM_V3_NEXT_PHASE_READINESS_REPORT_TYPE,
    TOM_V3_NEXT_PHASE_READINESS_REPORT_VERSION,
    build_tom_v3_expansion_completion_freeze,
    build_tom_v3_next_phase_readiness_report,
    validate_tom_v3_expansion_completion_freeze,
)


def test_build_tom_v3_expansion_completion_freeze_writes_stable_manifest(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "tom_v3_expansion_completion_freeze_v1.json"

    result = build_tom_v3_expansion_completion_freeze(
        output_path=output_path,
        current_main_commit=CURRENT_MAIN_COMMIT,
        generated_at=datetime(2026, 6, 18, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["freeze_type"] == TOM_V3_EXPANSION_COMPLETION_FREEZE_TYPE
    assert result["freeze_version"] == TOM_V3_EXPANSION_COMPLETION_FREEZE_VERSION
    assert result["completed_blueprint_count"] == 15
    assert result["frozen_contract_count"] == 11

    freeze = json.loads(output_path.read_text(encoding="utf-8"))
    assert freeze["generated_at"] == "2026-06-18T00:00:00+00:00"
    assert freeze["current_main_commit"] == CURRENT_MAIN_COMMIT
    assert freeze["latest_completed_blueprint"]["blueprint"] == "blueprint_36"
    assert len(freeze["completed_blueprints"]) == 15
    assert len(freeze["frozen_contract_refs"]) == len(FROZEN_CONTRACT_REFS)
    assert freeze["protected_baseline_refs"][1]["identifiers"] == PROTECTED_SAMPLE_POINT_IDS
    assert freeze["protected_baseline_refs"][1]["tracked_required"] is False
    assert (
        freeze["next_phase_recommendations"][0]["recommended_first_blueprint"]
        == "Gameplay Segment Gate / TOM v1 View Classifier Integration v1"
    )
    assert (
        freeze["next_phase_recommendations"][0]["existing_asset"]
        == "model_assets/tom_v1/view_classifier_gameplay.pt"
    )
    assert freeze["next_phase_recommendations"][0]["implementation_in_blueprint_37"] is False
    assert freeze["warnings"]["does_not_wire_gameplay_classifier"] is True
    assert not (FORBIDDEN_FREEZE_CLAIMS & _walk_exact_strings_and_keys(freeze))


def test_validate_tom_v3_expansion_completion_freeze_accepts_tracked_refs(
    tmp_path: Path,
) -> None:
    repo_root = _init_freeze_repo(tmp_path)
    freeze_path = repo_root / "freeze.json"
    validation_path = repo_root / "validation.json"
    build_tom_v3_expansion_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )

    result = validate_tom_v3_expansion_completion_freeze(
        freeze_path=freeze_path,
        output_path=validation_path,
        repo_root=repo_root,
        validated_at=datetime(2026, 6, 18, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert len(result["frozen_contract_validations"]) == len(FROZEN_CONTRACT_REFS)
    assert all(item["ok"] is True for item in result["frozen_contract_validations"])
    assert result["protected_baseline_validations"] == [
        {
            "ref_type": "protected_baseline_ref",
            "path": ".data/baselines/multi_point_regression_matrix.baseline.json",
            "exists": True,
            "tracked": True,
            "ok": True,
        }
    ]
    assert result["tracked_exports"] == []
    assert validation_path.is_file()


def test_validate_tom_v3_expansion_completion_freeze_rejects_forbidden_claims(
    tmp_path: Path,
) -> None:
    repo_root = _init_freeze_repo(tmp_path)
    freeze_path = repo_root / "freeze.json"
    build_tom_v3_expansion_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    freeze["validation_summary"]["correct"] = True
    freeze["warnings"]["claim_value"] = "adjudicated"
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")

    result = validate_tom_v3_expansion_completion_freeze(
        freeze_path=freeze_path,
        output_path=None,
        repo_root=repo_root,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert {error["error_type"] for error in result["errors"]} >= {
        "forbidden_claim_key",
        "forbidden_claim_value",
    }


def test_validate_tom_v3_expansion_completion_freeze_rejects_tracked_exports(
    tmp_path: Path,
) -> None:
    repo_root = _init_freeze_repo(tmp_path)
    export_path = repo_root / ".data" / "exports" / "generated_report.json"
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text("{}", encoding="utf-8")
    _run_git(repo_root, "add", ".data/exports/generated_report.json")
    _run_git(repo_root, "commit", "-m", "track generated export")
    freeze_path = repo_root / "freeze.json"
    build_tom_v3_expansion_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )

    result = validate_tom_v3_expansion_completion_freeze(
        freeze_path=freeze_path,
        output_path=None,
        repo_root=repo_root,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(error["error_type"] == "generated_exports_tracked" for error in result["errors"])


def test_build_tom_v3_next_phase_readiness_report_uses_freeze(
    tmp_path: Path,
) -> None:
    repo_root = _init_freeze_repo(tmp_path)
    freeze_path = repo_root / "freeze.json"
    report_path = repo_root / "readiness_report.json"
    build_tom_v3_expansion_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )

    result = build_tom_v3_next_phase_readiness_report(
        freeze_path=freeze_path,
        output_path=report_path,
        repo_root=repo_root,
        generated_at=datetime(2026, 6, 18, 18, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == TOM_V3_NEXT_PHASE_READINESS_REPORT_TYPE
    assert result["report_version"] == TOM_V3_NEXT_PHASE_READINESS_REPORT_VERSION
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-18T18:00:00+00:00"
    assert report["summary"]["completed_blueprint_count"] == 15
    assert report["summary"]["frozen_contract_count"] == 11
    assert report["summary"]["freeze_validation_status"] == "valid"
    assert report["readiness_assessment"]["ready_for_gameplay_segment_gate_blueprint"] is True
    assert (
        report["next_phase_recommendations"][0]["recommended_first_blueprint"]
        == "Gameplay Segment Gate / TOM v1 View Classifier Integration v1"
    )


def _init_freeze_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    _run_git(repo_root, "init")
    _run_git(repo_root, "config", "user.email", "codex@example.invalid")
    _run_git(repo_root, "config", "user.name", "Codex")

    for ref in FROZEN_CONTRACT_REFS:
        path = repo_root / ref
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"contract_ref": ref}), encoding="utf-8")

    baseline_path = repo_root / ".data" / "baselines" / (
        "multi_point_regression_matrix.baseline.json"
    )
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(
        json.dumps({"baseline_type": "multi_point_regression_matrix_baseline"}),
        encoding="utf-8",
    )

    _run_git(repo_root, "add", ".data/contracts", ".data/baselines")
    _run_git(repo_root, "commit", "-m", "seed tracked freeze refs")
    return repo_root


def _run_git(repo_root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def _walk_exact_strings_and_keys(value: Any) -> set[str]:
    seen: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            seen.add(str(key))
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            seen.update(_walk_exact_strings_and_keys(nested))
    elif isinstance(value, str):
        seen.add(value)
    return seen
