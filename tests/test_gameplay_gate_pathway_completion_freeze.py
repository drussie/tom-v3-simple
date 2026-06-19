from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.gameplay_gate_pathway_completion_freeze import (
    CURRENT_MAIN_COMMIT,
    FORBIDDEN_GAMEPLAY_FREEZE_CLAIMS,
    FROZEN_GAMEPLAY_CONTRACT_REFS,
    GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_TYPE,
    GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_VERSION,
    GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_TYPE,
    GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION,
    GAMEPLAY_GATE_REGRESSION_BASELINE_REF,
    build_gameplay_gate_next_phase_readiness_report,
    build_gameplay_gate_pathway_completion_freeze,
    validate_gameplay_gate_pathway_completion_freeze,
)


def test_build_gameplay_gate_pathway_completion_freeze_writes_stable_manifest(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "gameplay_gate_pathway_completion_freeze_v1.json"

    result = build_gameplay_gate_pathway_completion_freeze(
        output_path=output_path,
        current_main_commit=CURRENT_MAIN_COMMIT,
        generated_at=datetime(2026, 6, 19, 0, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["freeze_type"] == GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_TYPE
    assert result["freeze_version"] == GAMEPLAY_GATE_PATHWAY_COMPLETION_FREEZE_VERSION
    assert result["completed_gameplay_blueprint_count"] == 7
    assert result["frozen_gameplay_contract_count"] == 7

    freeze = json.loads(output_path.read_text(encoding="utf-8"))
    assert freeze["generated_at"] == "2026-06-19T00:00:00+00:00"
    assert freeze["current_main_commit"] == CURRENT_MAIN_COMMIT
    assert freeze["latest_completed_blueprint"]["blueprint"] == "blueprint_44"
    assert len(freeze["completed_gameplay_blueprints"]) == 7
    assert len(freeze["frozen_gameplay_contract_refs"]) == len(
        FROZEN_GAMEPLAY_CONTRACT_REFS
    )
    assert (
        freeze["protected_gameplay_baseline_refs"][0]["path"]
        == GAMEPLAY_GATE_REGRESSION_BASELINE_REF
    )
    assert (
        freeze["gameplay_classifier_asset_ref"]["path"]
        == "model_assets/tom_v1/view_classifier_gameplay.pt"
    )
    assert (
        freeze["next_phase_recommendations"][0]["recommended_blueprint"]
        == "Blueprint 46 - Real Broadcast Gameplay Gate Corpus Run v1"
    )
    assert freeze["next_phase_recommendations"][0]["implementation_in_blueprint_45"] is False
    assert freeze["warnings"]["does_not_mutate_model_assets"] is True
    assert not (FORBIDDEN_GAMEPLAY_FREEZE_CLAIMS & _walk_exact_strings_and_keys(freeze))


def test_validate_gameplay_gate_pathway_completion_freeze_accepts_tracked_refs(
    tmp_path: Path,
) -> None:
    repo_root = _init_gameplay_freeze_repo(tmp_path)
    freeze_path = repo_root / "freeze.json"
    validation_path = repo_root / "validation.json"
    build_gameplay_gate_pathway_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )

    result = validate_gameplay_gate_pathway_completion_freeze(
        freeze_path=freeze_path,
        output_path=validation_path,
        repo_root=repo_root,
        validated_at=datetime(2026, 6, 19, 12, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert len(result["frozen_gameplay_contract_validations"]) == len(
        FROZEN_GAMEPLAY_CONTRACT_REFS
    )
    assert all(item["ok"] is True for item in result["frozen_gameplay_contract_validations"])
    assert result["protected_gameplay_baseline_validations"] == [
        {
            "ref_type": "protected_gameplay_baseline_ref",
            "path": GAMEPLAY_GATE_REGRESSION_BASELINE_REF,
            "exists": True,
            "tracked": True,
            "ok": True,
        }
    ]
    assert result["gameplay_classifier_asset_validation"]["tracked"] is False
    assert result["gameplay_classifier_asset_validation"]["ok"] is True
    assert result["tracked_exports"] == []
    assert validation_path.is_file()


def test_validate_gameplay_gate_pathway_completion_freeze_rejects_forbidden_claims(
    tmp_path: Path,
) -> None:
    repo_root = _init_gameplay_freeze_repo(tmp_path)
    freeze_path = repo_root / "freeze.json"
    build_gameplay_gate_pathway_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    freeze["validation_summary"]["correct"] = True
    freeze["warnings"]["claim_value"] = "adjudicated"
    freeze_path.write_text(json.dumps(freeze), encoding="utf-8")

    result = validate_gameplay_gate_pathway_completion_freeze(
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


def test_validate_gameplay_gate_pathway_completion_freeze_rejects_tracked_model_asset(
    tmp_path: Path,
) -> None:
    repo_root = _init_gameplay_freeze_repo(tmp_path)
    _run_git(repo_root, "add", "model_assets/tom_v1/view_classifier_gameplay.pt")
    _run_git(repo_root, "commit", "-m", "track gameplay model asset")
    freeze_path = repo_root / "freeze.json"
    build_gameplay_gate_pathway_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )

    result = validate_gameplay_gate_pathway_completion_freeze(
        freeze_path=freeze_path,
        output_path=None,
        repo_root=repo_root,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    assert any(
        error["error_type"] == "model_asset_committed_or_modified"
        for error in result["errors"]
    )


def test_build_gameplay_gate_next_phase_readiness_report_uses_freeze(
    tmp_path: Path,
) -> None:
    repo_root = _init_gameplay_freeze_repo(tmp_path)
    freeze_path = repo_root / "freeze.json"
    report_path = repo_root / "readiness_report.json"
    build_gameplay_gate_pathway_completion_freeze(
        output_path=freeze_path,
        repo_root=repo_root,
        current_main_commit=CURRENT_MAIN_COMMIT,
    )

    result = build_gameplay_gate_next_phase_readiness_report(
        freeze_path=freeze_path,
        output_path=report_path,
        repo_root=repo_root,
        generated_at=datetime(2026, 6, 19, 18, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_TYPE
    assert result["report_version"] == GAMEPLAY_GATE_NEXT_PHASE_READINESS_REPORT_VERSION
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-19T18:00:00+00:00"
    assert report["summary"]["completed_gameplay_blueprint_count"] == 7
    assert report["summary"]["frozen_gameplay_contract_count"] == 7
    assert report["summary"]["freeze_validation_status"] == "valid"
    assert (
        report["readiness_assessment"]["ready_for_controlled_real_broadcast_corpus_run"]
        is True
    )
    assert report["readiness_assessment"]["does_not_implement_blueprint_46"] is True
    assert (
        report["next_phase_recommendations"][0]["recommended_blueprint"]
        == "Blueprint 46 - Real Broadcast Gameplay Gate Corpus Run v1"
    )


def _init_gameplay_freeze_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    _run_git(repo_root, "init")
    _run_git(repo_root, "config", "user.email", "codex@example.invalid")
    _run_git(repo_root, "config", "user.name", "Codex")

    for ref in FROZEN_GAMEPLAY_CONTRACT_REFS:
        path = repo_root / ref
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"contract_ref": ref}), encoding="utf-8")

    baseline_path = repo_root / GAMEPLAY_GATE_REGRESSION_BASELINE_REF
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(
        json.dumps({"baseline_type": "gameplay_gate_regression_baseline"}),
        encoding="utf-8",
    )

    earlier_freeze = (
        repo_root / ".data" / "contracts" / "tom_v3_expansion_completion_freeze_v1.json"
    )
    earlier_freeze.write_text(
        json.dumps({"freeze_type": "tom_v3_expansion_completion_freeze"}),
        encoding="utf-8",
    )

    model_asset = repo_root / "model_assets" / "tom_v1" / "view_classifier_gameplay.pt"
    model_asset.parent.mkdir(parents=True, exist_ok=True)
    model_asset.write_bytes(b"local ignored gameplay model")

    _run_git(repo_root, "add", ".data/contracts", ".data/baselines")
    _run_git(repo_root, "commit", "-m", "seed tracked gameplay freeze refs")
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
        for item in value:
            seen.update(_walk_exact_strings_and_keys(item))
    elif isinstance(value, str):
        seen.add(value)
    return seen
