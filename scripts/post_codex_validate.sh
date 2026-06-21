#!/usr/bin/env bash
set -euo pipefail

EXPECTED_BRANCH=""
EXPECTED_TAG=""
PYTHON_BIN=".venv/bin/python"
TMP_ROOT=".data/tmp/post_codex_validate"

usage() {
  cat <<'EOF'
Usage: scripts/post_codex_validate.sh [--branch <branch>] [--expected-tag <tag>] [--python <python>]

Runs validation only. This script does not merge, commit, tag, push, clean files, or modify git
state. Temporary validation artifacts are written under .data/tmp/post_codex_validate.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      EXPECTED_BRANCH="${2:-}"
      shift 2
      ;;
    --expected-tag)
      EXPECTED_TAG="${2:-}"
      shift 2
      ;;
    --python)
      PYTHON_BIN="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

run() {
  echo "+ $*"
  "$@"
}

run_shell() {
  echo "+ $*"
  bash -lc "$*"
}

CURRENT_BRANCH="$(git branch --show-current)"
if [[ -n "$EXPECTED_BRANCH" && "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]]; then
  echo "Expected branch '$EXPECTED_BRANCH' but current branch is '$CURRENT_BRANCH'" >&2
  exit 1
fi

if [[ -n "$EXPECTED_TAG" ]]; then
  run git rev-parse --verify --quiet "refs/tags/$EXPECTED_TAG"
fi

mkdir -p "$TMP_ROOT"

run "$PYTHON_BIN" -m pytest -q
run "$PYTHON_BIN" -m ruff check .
run git diff --check

run_shell "cd apps/web && npm run lint && npm run build && npm audit --omit=dev"

run make tom-v1-build-multi-point-replay-index \
  PYTHON="$PYTHON_BIN" \
  MULTI_POINT_REPLAY_INDEX_OUTPUT="$TMP_ROOT/multi_point_replay_index.json"

run env TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
  make tom-v1-verify-multi-point-regression-matrix \
  PYTHON="$PYTHON_BIN" \
  MULTI_POINT_REPLAY_INDEX_OUTPUT="$TMP_ROOT/multi_point_replay_index.json" \
  MULTI_POINT_REGRESSION_MATRIX_CURRENT="$TMP_ROOT/multi_point_regression_matrix.current.json" \
  MULTI_POINT_REGRESSION_MATRIX_REGRESSION="$TMP_ROOT/multi_point_regression_matrix.regression.json" \
  MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN="$TMP_ROOT/multi_point_regression_matrix.regression.md"

run env TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
  make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON="$PYTHON_BIN" \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97 \
  CURRENT_OUTPUT="$TMP_ROOT/reviewed_3d_debug_dataset_sample_point.current.json" \
  REGRESSION="$TMP_ROOT/reviewed_3d_debug_dataset_sample_point.regression.json" \
  REGRESSION_MARKDOWN="$TMP_ROOT/reviewed_3d_debug_dataset_sample_point.regression.md"

run "$PYTHON_BIN" -m apps.worker.cli export-observation-quality-taxonomy \
  --output "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-review-label-schema \
  --output "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-reviewer-confidence-schema \
  --output "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-reviewer-confidence-template \
  --point-manifest-id point_manifest_v0_690dfd41205609e0caca1263 \
  --media-id 9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  --replay-url "http://127.0.0.1:3000/replay/9518fb01-0da1-4344-9a84-ff88ec8e9b1e" \
  --event-candidate-run-id 1b946366-7ec1-426f-8b40-494535a9b3fb \
  --trajectory-3d-run-id ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  --camera-geometry-id 5afa67fb-7f6e-41eb-b4aa-b1100a97ee97 \
  --output "$TMP_ROOT/reviewer_confidence_ambiguity_template.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-reviewer-confidence-bundle \
  --schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --bundle "$TMP_ROOT/reviewer_confidence_ambiguity_template.current.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --output "$TMP_ROOT/reviewer_confidence_ambiguity.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-multi-reviewer-disagreement-schema \
  --output "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-intennse-label-alignment-contract \
  --output "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-intennse-alignment-template \
  --point-manifest-id point_manifest_v0_690dfd41205609e0caca1263 \
  --media-id 9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  --replay-url "http://127.0.0.1:3000/replay/9518fb01-0da1-4344-9a84-ff88ec8e9b1e" \
  --event-candidate-run-id 1b946366-7ec1-426f-8b40-494535a9b3fb \
  --trajectory-3d-run-id ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  --camera-geometry-id 5afa67fb-7f6e-41eb-b4aa-b1100a97ee97 \
  --tom-reviewer-confidence-bundle-ref "$TMP_ROOT/reviewer_confidence_ambiguity_template.current.json" \
  --intennse-label-bundle-ref "intennse://placeholder/expert-label-bundle" \
  --intennse-schema-version "placeholder-v1" \
  --output "$TMP_ROOT/intennse_alignment_template.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-intennse-alignment-bundle \
  --contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --bundle "$TMP_ROOT/intennse_alignment_template.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --output "$TMP_ROOT/intennse_alignment_bundle.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-intennse-alignment-report \
  --contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --bundle "$TMP_ROOT/intennse_alignment_template.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --output "$TMP_ROOT/intennse_alignment_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-versioned-dataset-corpus-contract \
  --output "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-versioned-dataset-corpus-manifest \
  --index "$TMP_ROOT/multi_point_replay_index.json" \
  --matrix "$TMP_ROOT/multi_point_regression_matrix.current.json" \
  --output "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-versioned-dataset-corpus-manifest \
  --contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --output "$TMP_ROOT/versioned_dataset_corpus_manifest.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-versioned-dataset-corpus-report \
  --contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --output "$TMP_ROOT/versioned_dataset_corpus_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-coverage-sampling-strategy-contract \
  --output "$TMP_ROOT/coverage_sampling_strategy_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-coverage-sampling-profile \
  --corpus-manifest "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --index "$TMP_ROOT/multi_point_replay_index.json" \
  --matrix "$TMP_ROOT/multi_point_regression_matrix.current.json" \
  --output "$TMP_ROOT/coverage_sampling_profile.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-coverage-sampling-profile \
  --contract "$TMP_ROOT/coverage_sampling_strategy_contract_v1.smoke.json" \
  --profile "$TMP_ROOT/coverage_sampling_profile.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --dataset-corpus-contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --output "$TMP_ROOT/coverage_sampling_profile.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-coverage-sampling-report \
  --contract "$TMP_ROOT/coverage_sampling_strategy_contract_v1.smoke.json" \
  --profile "$TMP_ROOT/coverage_sampling_profile.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --dataset-corpus-contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --output "$TMP_ROOT/coverage_sampling_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-many-point-ingestion-gate-contract \
  --output "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-many-point-ingestion-manifest-template \
  --local-media-path "demo_assets/sample_point.mp4" \
  --source-label "post_codex_demo_local_point_video" \
  --output "$TMP_ROOT/many_point_ingestion_manifest.template.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-many-point-ingestion-manifest \
  --contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/many_point_ingestion_manifest.template.json" \
  --output "$TMP_ROOT/many_point_ingestion_manifest.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-many-point-ingestion-plan \
  --contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/many_point_ingestion_manifest.template.json" \
  --mode dry_run \
  --output "$TMP_ROOT/many_point_ingestion_plan.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli run-many-point-ingestion-gate \
  --contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/many_point_ingestion_manifest.template.json" \
  --mode dry_run \
  --output "$TMP_ROOT/many_point_ingestion_gate.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-review-ops-metrics-contract \
  --output "$TMP_ROOT/review_ops_metrics_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-ops-metrics-report \
  --contract "$TMP_ROOT/review_ops_metrics_contract_v1.smoke.json" \
  --corpus-manifest "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --coverage-sampling-profile "$TMP_ROOT/coverage_sampling_profile.current.json" \
  --coverage-sampling-report "$TMP_ROOT/coverage_sampling_report.current.json" \
  --many-point-ingestion-gate "$TMP_ROOT/many_point_ingestion_gate.current.json" \
  --output "$TMP_ROOT/review_ops_metrics_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-review-ops-metrics-report \
  --contract "$TMP_ROOT/review_ops_metrics_contract_v1.smoke.json" \
  --report "$TMP_ROOT/review_ops_metrics_report.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --dataset-corpus-contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --coverage-sampling-contract "$TMP_ROOT/coverage_sampling_strategy_contract_v1.smoke.json" \
  --many-point-ingestion-contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --output "$TMP_ROOT/review_ops_metrics_report.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-ops-dashboard-data \
  --report "$TMP_ROOT/review_ops_metrics_report.current.json" \
  --output "$TMP_ROOT/review_ops_dashboard_data.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-label-feedback-evaluation-contract \
  --output "$TMP_ROOT/label_feedback_evaluation_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-label-feedback-evaluation-inputs \
  --contract "$TMP_ROOT/label_feedback_evaluation_contract_v1.smoke.json" \
  --corpus-manifest "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --review-ops-metrics-report "$TMP_ROOT/review_ops_metrics_report.current.json" \
  --review-ops-dashboard-data "$TMP_ROOT/review_ops_dashboard_data.current.json" \
  --coverage-sampling-profile "$TMP_ROOT/coverage_sampling_profile.current.json" \
  --coverage-sampling-report "$TMP_ROOT/coverage_sampling_report.current.json" \
  --multi-point-regression-matrix "$TMP_ROOT/multi_point_regression_matrix.current.json" \
  --output "$TMP_ROOT/label_feedback_evaluation_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-label-feedback-evaluation-inputs \
  --contract "$TMP_ROOT/label_feedback_evaluation_contract_v1.smoke.json" \
  --feedback-inputs "$TMP_ROOT/label_feedback_evaluation_inputs.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --dataset-corpus-contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --coverage-sampling-contract "$TMP_ROOT/coverage_sampling_strategy_contract_v1.smoke.json" \
  --many-point-ingestion-contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --review-ops-metrics-contract "$TMP_ROOT/review_ops_metrics_contract_v1.smoke.json" \
  --output "$TMP_ROOT/label_feedback_evaluation_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-label-feedback-evaluation-report \
  --contract "$TMP_ROOT/label_feedback_evaluation_contract_v1.smoke.json" \
  --feedback-inputs "$TMP_ROOT/label_feedback_evaluation_inputs.current.json" \
  --output "$TMP_ROOT/label_feedback_evaluation_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-camera-geometry-calibration-provenance-contract \
  --output "$TMP_ROOT/camera_geometry_calibration_provenance_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-camera-geometry-calibration-profile \
  --contract "$TMP_ROOT/camera_geometry_calibration_provenance_contract_v1.smoke.json" \
  --replay-index "$TMP_ROOT/multi_point_replay_index.json" \
  --regression-matrix "$TMP_ROOT/multi_point_regression_matrix.current.json" \
  --corpus-manifest "$TMP_ROOT/versioned_dataset_corpus_manifest.current.json" \
  --label-feedback-inputs "$TMP_ROOT/label_feedback_evaluation_inputs.current.json" \
  --output "$TMP_ROOT/camera_geometry_calibration_profile.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-camera-geometry-calibration-profile \
  --contract "$TMP_ROOT/camera_geometry_calibration_provenance_contract_v1.smoke.json" \
  --profile "$TMP_ROOT/camera_geometry_calibration_profile.current.json" \
  --observation-quality-taxonomy "$TMP_ROOT/observation_quality_taxonomy_v1.smoke.json" \
  --review-label-schema "$TMP_ROOT/review_label_schema_v1.smoke.json" \
  --reviewer-confidence-schema "$TMP_ROOT/reviewer_confidence_ambiguity_schema_v1.smoke.json" \
  --multi-reviewer-schema "$TMP_ROOT/multi_reviewer_disagreement_schema_v1.smoke.json" \
  --intennse-alignment-contract "$TMP_ROOT/intennse_label_alignment_contract_v1.smoke.json" \
  --dataset-corpus-contract "$TMP_ROOT/versioned_dataset_corpus_contract_v1.smoke.json" \
  --coverage-sampling-contract "$TMP_ROOT/coverage_sampling_strategy_contract_v1.smoke.json" \
  --many-point-ingestion-contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --review-ops-metrics-contract "$TMP_ROOT/review_ops_metrics_contract_v1.smoke.json" \
  --label-feedback-contract "$TMP_ROOT/label_feedback_evaluation_contract_v1.smoke.json" \
  --output "$TMP_ROOT/camera_geometry_calibration_profile.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-camera-geometry-calibration-report \
  --contract "$TMP_ROOT/camera_geometry_calibration_provenance_contract_v1.smoke.json" \
  --profile "$TMP_ROOT/camera_geometry_calibration_profile.current.json" \
  --output "$TMP_ROOT/camera_geometry_calibration_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-tom-v3-expansion-completion-freeze \
  --output "$TMP_ROOT/tom_v3_expansion_completion_freeze_v1.smoke.json" \
  --current-main-commit bb90aac8 \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-tom-v3-expansion-completion-freeze \
  --freeze "$TMP_ROOT/tom_v3_expansion_completion_freeze_v1.smoke.json" \
  --output "$TMP_ROOT/tom_v3_expansion_completion_freeze.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-tom-v3-next-phase-readiness-report \
  --freeze "$TMP_ROOT/tom_v3_expansion_completion_freeze_v1.smoke.json" \
  --output "$TMP_ROOT/tom_v3_next_phase_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-segment-gate-contract \
  --output "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli inspect-gameplay-classifier-asset \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/gameplay_classifier_asset_inspection.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-segment-candidates \
  --local-media-path "demo_assets/sample_point.mp4" \
  --media-id "sample_point_gameplay_segment_gate_smoke" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/gameplay_segment_candidates.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-segment-candidates \
  --contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --candidates "$TMP_ROOT/gameplay_segment_candidates.current.json" \
  --output "$TMP_ROOT/gameplay_segment_candidates.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-segment-report \
  --contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --candidates "$TMP_ROOT/gameplay_segment_candidates.current.json" \
  --output "$TMP_ROOT/gameplay_segment_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-gated-routing-contract \
  --output "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gated-routing-plan \
  --gameplay-segments "$TMP_ROOT/gameplay_segment_candidates.current.json" \
  --gameplay-segment-contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --output "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --routing-mode "dry_run" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-gated-routing-plan \
  --contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --gameplay-segment-contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --output "$TMP_ROOT/gameplay_gated_routing_plan.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gated-routing-report \
  --contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --gameplay-segment-contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --output "$TMP_ROOT/gameplay_gated_routing_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-gated-perception-execution-contract \
  --output "$TMP_ROOT/gameplay_gated_perception_execution_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gated-perception-execution-plan \
  --routing-plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --routing-contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --output "$TMP_ROOT/gameplay_gated_perception_execution_plan.current.json" \
  --execution-mode "dry_run" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-gated-perception-execution-plan \
  --contract "$TMP_ROOT/gameplay_gated_perception_execution_contract_v1.smoke.json" \
  --plan "$TMP_ROOT/gameplay_gated_perception_execution_plan.current.json" \
  --routing-contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --routing-plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --output "$TMP_ROOT/gameplay_gated_perception_execution_plan.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gated-perception-execution-report \
  --contract "$TMP_ROOT/gameplay_gated_perception_execution_contract_v1.smoke.json" \
  --plan "$TMP_ROOT/gameplay_gated_perception_execution_plan.current.json" \
  --routing-contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --routing-plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --output "$TMP_ROOT/gameplay_gated_perception_execution_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-segment-replay-review-contract \
  --output "$TMP_ROOT/gameplay_segment_replay_review_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-segment-replay-timeline \
  --gameplay-segments "$TMP_ROOT/gameplay_segment_candidates.current.json" \
  --routing-plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --execution-plan "$TMP_ROOT/gameplay_gated_perception_execution_plan.current.json" \
  --output "$TMP_ROOT/gameplay_segment_replay_timeline.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-segment-replay-timeline \
  --contract "$TMP_ROOT/gameplay_segment_replay_review_contract_v1.smoke.json" \
  --timeline "$TMP_ROOT/gameplay_segment_replay_timeline.current.json" \
  --gameplay-segments "$TMP_ROOT/gameplay_segment_candidates.current.json" \
  --routing-plan "$TMP_ROOT/gameplay_gated_routing_plan.current.json" \
  --execution-plan "$TMP_ROOT/gameplay_gated_perception_execution_plan.current.json" \
  --output "$TMP_ROOT/gameplay_segment_replay_timeline.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-segment-review-template \
  --timeline "$TMP_ROOT/gameplay_segment_replay_timeline.current.json" \
  --output "$TMP_ROOT/gameplay_segment_review_template.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-segment-review-bundle \
  --contract "$TMP_ROOT/gameplay_segment_replay_review_contract_v1.smoke.json" \
  --bundle "$TMP_ROOT/gameplay_segment_review_template.current.json" \
  --timeline "$TMP_ROOT/gameplay_segment_replay_timeline.current.json" \
  --output "$TMP_ROOT/gameplay_segment_review_bundle.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-segment-review-report \
  --contract "$TMP_ROOT/gameplay_segment_replay_review_contract_v1.smoke.json" \
  --timeline "$TMP_ROOT/gameplay_segment_replay_timeline.current.json" \
  --bundle "$TMP_ROOT/gameplay_segment_review_template.current.json" \
  --output "$TMP_ROOT/gameplay_segment_review_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-gated-many-point-smoke-contract \
  --output "$TMP_ROOT/gameplay_gated_many_point_smoke_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gated-many-point-smoke-manifest-template \
  --local-media-path "demo_assets/sample_point.mp4" \
  --local-media-path "demo_assets/sample_point.mp4" \
  --source-label "post_codex_gameplay_gated_smoke" \
  --output "$TMP_ROOT/gameplay_gated_many_point_smoke_manifest.template.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-gated-many-point-smoke-manifest \
  --contract "$TMP_ROOT/gameplay_gated_many_point_smoke_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/gameplay_gated_many_point_smoke_manifest.template.json" \
  --output "$TMP_ROOT/gameplay_gated_many_point_smoke_manifest.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli run-gameplay-gated-many-point-smoke \
  --contract "$TMP_ROOT/gameplay_gated_many_point_smoke_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/gameplay_gated_many_point_smoke_manifest.template.json" \
  --smoke-mode "fixture_only" \
  --output-dir "$TMP_ROOT/gameplay_gated_many_point_smoke_outputs" \
  --output "$TMP_ROOT/gameplay_gated_many_point_smoke.current.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --many-point-contract "$TMP_ROOT/many_point_ingestion_gate_contract_v1.smoke.json" \
  --gameplay-segment-contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --routing-contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --execution-contract "$TMP_ROOT/gameplay_gated_perception_execution_contract_v1.smoke.json" \
  --replay-review-contract "$TMP_ROOT/gameplay_segment_replay_review_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gated-many-point-smoke-report \
  --contract "$TMP_ROOT/gameplay_gated_many_point_smoke_contract_v1.smoke.json" \
  --smoke-report "$TMP_ROOT/gameplay_gated_many_point_smoke.current.json" \
  --output "$TMP_ROOT/gameplay_gated_many_point_smoke_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-gate-regression-baseline-contract \
  --output "$TMP_ROOT/gameplay_gate_regression_baseline_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gate-regression-baseline \
  --contract "$TMP_ROOT/gameplay_gate_regression_baseline_contract_v1.smoke.json" \
  --work-dir "$TMP_ROOT/gameplay_gate_regression" \
  --fixture-media-path "demo_assets/sample_point.mp4" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli verify-gameplay-gate-regression-baseline \
  --contract "$TMP_ROOT/gameplay_gate_regression_baseline_contract_v1.smoke.json" \
  --baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --work-dir "$TMP_ROOT/gameplay_gate_regression" \
  --fixture-media-path "demo_assets/sample_point.mp4" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/gameplay_gate_regression.verification.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gate-regression-report \
  --contract "$TMP_ROOT/gameplay_gate_regression_baseline_contract_v1.smoke.json" \
  --baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --verification "$TMP_ROOT/gameplay_gate_regression.verification.json" \
  --output "$TMP_ROOT/gameplay_gate_regression.report.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-gameplay-gate-review-dataset-contract \
  --output "$TMP_ROOT/gameplay_gate_review_dataset_export_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gate-review-dataset \
  --contract "$TMP_ROOT/gameplay_gate_review_dataset_export_contract_v1.smoke.json" \
  --work-dir "$TMP_ROOT/gameplay_gate_review_dataset" \
  --fixture-media-path "demo_assets/sample_point.mp4" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --regression-verification "$TMP_ROOT/gameplay_gate_regression.verification.json" \
  --output "$TMP_ROOT/gameplay_gate_review_dataset.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-gate-review-dataset \
  --contract "$TMP_ROOT/gameplay_gate_review_dataset_export_contract_v1.smoke.json" \
  --dataset "$TMP_ROOT/gameplay_gate_review_dataset.current.json" \
  --output "$TMP_ROOT/gameplay_gate_review_dataset.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gate-review-dataset-report \
  --contract "$TMP_ROOT/gameplay_gate_review_dataset_export_contract_v1.smoke.json" \
  --dataset "$TMP_ROOT/gameplay_gate_review_dataset.current.json" \
  --output "$TMP_ROOT/gameplay_gate_review_dataset.report.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gate-pathway-completion-freeze \
  --output "$TMP_ROOT/gameplay_gate_pathway_completion_freeze_v1.smoke.json" \
  --current-main-commit 6d0f5441 \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-gameplay-gate-pathway-completion-freeze \
  --freeze "$TMP_ROOT/gameplay_gate_pathway_completion_freeze_v1.smoke.json" \
  --output "$TMP_ROOT/gameplay_gate_pathway_completion_freeze.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-gameplay-gate-next-phase-readiness-report \
  --freeze "$TMP_ROOT/gameplay_gate_pathway_completion_freeze_v1.smoke.json" \
  --output "$TMP_ROOT/gameplay_gate_next_phase_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-real-broadcast-gameplay-corpus-run-contract \
  --output "$TMP_ROOT/real_broadcast_gameplay_corpus_run_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-corpus-manifest-template \
  --local-media-path "demo_assets/sample_point.mp4" \
  --source-label "post_codex_real_broadcast_fixture_clip" \
  --expected-broadcast-content-tag "live_gameplay" \
  --allow-fixture-mode \
  --output "$TMP_ROOT/real_broadcast_gameplay_corpus_manifest.template.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-real-broadcast-gameplay-corpus-manifest \
  --contract "$TMP_ROOT/real_broadcast_gameplay_corpus_run_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/real_broadcast_gameplay_corpus_manifest.template.json" \
  --run-mode "fixture_only" \
  --output "$TMP_ROOT/real_broadcast_gameplay_corpus_manifest.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli run-real-broadcast-gameplay-corpus \
  --contract "$TMP_ROOT/real_broadcast_gameplay_corpus_run_contract_v1.smoke.json" \
  --manifest "$TMP_ROOT/real_broadcast_gameplay_corpus_manifest.template.json" \
  --run-mode "fixture_only" \
  --output-dir "$TMP_ROOT/real_broadcast_gameplay_corpus_run" \
  --output "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --gameplay-segment-contract "$TMP_ROOT/gameplay_segment_gate_contract_v1.smoke.json" \
  --routing-contract "$TMP_ROOT/gameplay_gated_pipeline_routing_contract_v1.smoke.json" \
  --execution-contract "$TMP_ROOT/gameplay_gated_perception_execution_contract_v1.smoke.json" \
  --replay-review-contract "$TMP_ROOT/gameplay_segment_replay_review_contract_v1.smoke.json" \
  --review-dataset-contract "$TMP_ROOT/gameplay_gate_review_dataset_export_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-corpus-report \
  --contract "$TMP_ROOT/real_broadcast_gameplay_corpus_run_contract_v1.smoke.json" \
  --corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_corpus_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-real-broadcast-gameplay-review-loop-contract \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_loop_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-review-bundle-template \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_loop_contract_v1.smoke.json" \
  --source-corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --source-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-real-broadcast-gameplay-review-bundle \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_loop_contract_v1.smoke.json" \
  --bundle "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_bundle.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-review-loop-report \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_loop_contract_v1.smoke.json" \
  --bundle "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_loop_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-human-review-readiness-report \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_loop_contract_v1.smoke.json" \
  --bundle "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_human_review_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-real-broadcast-gameplay-review-metrics-contract \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_metrics_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-review-metrics-report \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_metrics_contract_v1.smoke.json" \
  --source-review-loop-report "$TMP_ROOT/real_broadcast_gameplay_review_loop_report.current.json" \
  --source-review-bundle "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --source-corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --source-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-real-broadcast-gameplay-review-metrics-report \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_metrics_contract_v1.smoke.json" \
  --metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-review-qa-dashboard \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_metrics_contract_v1.smoke.json" \
  --metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_qa_dashboard.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-review-next-actions-report \
  --contract "$TMP_ROOT/real_broadcast_gameplay_review_metrics_contract_v1.smoke.json" \
  --metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_review_next_actions.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-review-guided-gameplay-calibration-proposal-contract \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_proposal_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-inputs \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_proposal_contract_v1.smoke.json" \
  --source-metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --source-review-loop-report "$TMP_ROOT/real_broadcast_gameplay_review_loop_report.current.json" \
  --source-review-bundle "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --source-review-dataset "$TMP_ROOT/gameplay_gate_review_dataset.current.json" \
  --source-corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --source-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-review-guided-gameplay-calibration-inputs \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_proposal_contract_v1.smoke.json" \
  --calibration-inputs "$TMP_ROOT/review_guided_gameplay_calibration_inputs.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-proposal \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_proposal_contract_v1.smoke.json" \
  --calibration-inputs "$TMP_ROOT/review_guided_gameplay_calibration_inputs.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_proposal.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-review-guided-gameplay-calibration-proposal \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_proposal_contract_v1.smoke.json" \
  --calibration-proposal "$TMP_ROOT/review_guided_gameplay_calibration_proposal.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_proposal.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-proposal-report \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_proposal_contract_v1.smoke.json" \
  --calibration-proposal "$TMP_ROOT/review_guided_gameplay_calibration_proposal.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_proposal_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-review-guided-gameplay-calibration-evaluation-sandbox-contract \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-evaluation-inputs \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --source-calibration-proposal "$TMP_ROOT/review_guided_gameplay_calibration_proposal.current.json" \
  --source-metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --source-review-loop-report "$TMP_ROOT/real_broadcast_gameplay_review_loop_report.current.json" \
  --source-review-bundle "$TMP_ROOT/real_broadcast_gameplay_review_bundle.template.json" \
  --source-corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --source-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-review-guided-gameplay-calibration-evaluation-inputs \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --evaluation-inputs "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_inputs.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli run-review-guided-gameplay-calibration-evaluation-sandbox \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --evaluation-inputs "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_inputs.current.json" \
  --evaluation-mode "structural_offline_evaluation" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-review-guided-gameplay-calibration-evaluation-report \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-evaluation-summary \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_summary.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-review-guided-gameplay-calibration-sandbox-regression-contract \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_sandbox_regression_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-sandbox-regression-baseline \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_sandbox_regression_contract_v1.smoke.json" \
  --source-evaluation-inputs "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_inputs.current.json" \
  --source-evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --source-evaluation-contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli verify-review-guided-gameplay-calibration-sandbox-regression-baseline \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_sandbox_regression_contract_v1.smoke.json" \
  --baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --source-evaluation-inputs "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_inputs.current.json" \
  --source-evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --source-evaluation-contract "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.smoke.json" \
  --current-output "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.current.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.regression.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-review-guided-gameplay-calibration-sandbox-regression-report \
  --contract "$TMP_ROOT/review_guided_gameplay_calibration_sandbox_regression_contract_v1.smoke.json" \
  --baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --verification "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.regression.json" \
  --output "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.report.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-calibration-candidate-decision-packet-contract \
  --output "$TMP_ROOT/calibration_candidate_decision_packet_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-decision-packet-inputs \
  --contract "$TMP_ROOT/calibration_candidate_decision_packet_contract_v1.smoke.json" \
  --source-calibration-proposal "$TMP_ROOT/review_guided_gameplay_calibration_proposal.current.json" \
  --source-sandbox-evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --source-sandbox-regression-verification "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.regression.json" \
  --source-review-metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --source-review-loop-report "$TMP_ROOT/real_broadcast_gameplay_review_loop_report.current.json" \
  --source-corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/calibration_candidate_decision_packet_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-calibration-candidate-decision-packet-inputs \
  --contract "$TMP_ROOT/calibration_candidate_decision_packet_contract_v1.smoke.json" \
  --packet-inputs "$TMP_ROOT/calibration_candidate_decision_packet_inputs.current.json" \
  --output "$TMP_ROOT/calibration_candidate_decision_packet_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-decision-packet \
  --contract "$TMP_ROOT/calibration_candidate_decision_packet_contract_v1.smoke.json" \
  --packet-inputs "$TMP_ROOT/calibration_candidate_decision_packet_inputs.current.json" \
  --output "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-calibration-candidate-decision-packet \
  --contract "$TMP_ROOT/calibration_candidate_decision_packet_contract_v1.smoke.json" \
  --decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --output "$TMP_ROOT/calibration_candidate_decision_packet.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-decision-packet-report \
  --contract "$TMP_ROOT/calibration_candidate_decision_packet_contract_v1.smoke.json" \
  --decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --output "$TMP_ROOT/calibration_candidate_decision_packet.report.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-calibration-candidate-config-freeze-contract \
  --output "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-config-freeze-inputs \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-sandbox-evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --source-sandbox-regression-verification "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.regression.json" \
  --source-calibration-proposal "$TMP_ROOT/review_guided_gameplay_calibration_proposal.current.json" \
  --source-review-metrics-report "$TMP_ROOT/real_broadcast_gameplay_review_metrics_report.current.json" \
  --source-review-loop-report "$TMP_ROOT/real_broadcast_gameplay_review_loop_report.current.json" \
  --source-corpus-run "$TMP_ROOT/real_broadcast_gameplay_corpus_run.current.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/calibration_candidate_config_freeze_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-calibration-candidate-config-freeze-inputs \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --freeze-inputs "$TMP_ROOT/calibration_candidate_config_freeze_inputs.current.json" \
  --output "$TMP_ROOT/calibration_candidate_config_freeze_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-config-freeze \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --freeze-inputs "$TMP_ROOT/calibration_candidate_config_freeze_inputs.current.json" \
  --output "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-calibration-candidate-config-freeze \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --output "$TMP_ROOT/calibration_candidate_config_freeze.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-manual-approval-packet \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --output "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-calibration-candidate-manual-approval-packet \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --output "$TMP_ROOT/calibration_candidate_manual_approval_packet.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-calibration-candidate-config-freeze-report \
  --contract "$TMP_ROOT/calibration_candidate_config_freeze_contract_v1.smoke.json" \
  --candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --output "$TMP_ROOT/calibration_candidate_config_freeze.report.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-calibration-decision-phase-freeze \
  --candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-real-broadcast-gameplay-calibration-decision-phase-freeze \
  --freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-real-broadcast-gameplay-calibration-next-phase-readiness-report \
  --freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --output "$TMP_ROOT/real_broadcast_gameplay_calibration_next_phase_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-change-request-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-change-request-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-sandbox-evaluation-report "$TMP_ROOT/review_guided_gameplay_calibration_evaluation_report.current.json" \
  --source-sandbox-regression-verification "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.regression.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-change-request-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --change-request-inputs "$TMP_ROOT/controlled_runtime_calibration_change_request_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-change-request \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --change-request-inputs "$TMP_ROOT/controlled_runtime_calibration_change_request_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-change-request \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-change-request-dry-run \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request_dry_run.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-change-request-dry-run \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --dry-run "$TMP_ROOT/controlled_runtime_calibration_change_request_dry_run.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request_dry_run.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-change-request-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_change_request_contract_v1.smoke.json" \
  --change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --dry-run "$TMP_ROOT/controlled_runtime_calibration_change_request_dry_run.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_change_request.report.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-dry-run-execution-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-dry-run-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --dry-run-inputs "$TMP_ROOT/controlled_runtime_calibration_dry_run_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli run-controlled-runtime-calibration-dry-run \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --dry-run-inputs "$TMP_ROOT/controlled_runtime_calibration_dry_run_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-dry-run-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --dry-run-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-summary \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --dry-run-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_summary.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-rollback-readiness-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution_contract_v1.smoke.json" \
  --dry-run-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_rollback_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-dry-run-review-packet-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-review-packet-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-dry-run-inputs "$TMP_ROOT/controlled_runtime_calibration_dry_run_inputs.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-dry-run-review-packet-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --review-packet-inputs "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-review-packet \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --review-packet-inputs "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-dry-run-review-packet \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-review-summary \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_summary.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-dry-run-operator-checklist \
  --contract "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_dry_run_operator_checklist.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-human-approval-gate-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-human-approval-gate-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --source-dry-run-review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-human-approval-gate-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --approval-gate-inputs "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-human-approval-gate \
  --contract "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --approval-gate-inputs "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-human-approval-gate \
  --contract "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-human-approval-summary \
  --contract "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_human_approval_summary.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-future-application-readiness-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate_contract_v1.smoke.json" \
  --approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_future_application_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-application-plan-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-application-plan-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --source-human-approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --source-dry-run-review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_plan_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-application-plan-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --application-plan-inputs "$TMP_ROOT/controlled_runtime_calibration_application_plan_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_plan_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-application-plan \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --application-plan-inputs "$TMP_ROOT/controlled_runtime_calibration_application_plan_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-application-plan \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_plan.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-pre-application-gate-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_application_gate_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-rollback-plan-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_rollback_plan_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-post-application-verification-plan \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_plan_contract_v1.smoke.json" \
  --application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_post_application_verification_plan.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-runtime-application-staging-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-runtime-application-staging-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --source-application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --source-human-approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --source-dry-run-review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-runtime-application-staging-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging-inputs "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-runtime-application-staging \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging-inputs "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-runtime-application-staging \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-staged-config-delta \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_staged_config_delta.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-staged-config-delta \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staged-config-delta "$TMP_ROOT/controlled_runtime_calibration_staged_config_delta.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_staged_config_delta.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-pre-apply-manifest \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_apply_manifest.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-staged-rollback-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_staged_rollback_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-staged-post-application-verification-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging_contract_v1.smoke.json" \
  --staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_staged_post_application_verification_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-pre-application-final-gate-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-pre-application-final-gate-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --source-runtime-application-staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --source-application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --source-human-approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --source-dry-run-review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-pre-application-final-gate-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate-inputs "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-pre-application-final-gate \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate-inputs "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-pre-application-final-gate \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-final-gate-readiness-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_final_gate_readiness_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-final-gate-blocker-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_final_gate_blocker_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-final-gate-artifact-checklist \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_final_gate_artifact_checklist.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-final-gate-regression-checklist \
  --contract "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate_contract_v1.smoke.json" \
  --final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_final_gate_regression_checklist.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-application-execution-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-applied-runtime-config \
  --output "$TMP_ROOT/controlled_runtime_calibration_applied_runtime_config_v1.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-application-execution-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --source-pre-application-final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --source-runtime-application-staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --source-application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --source-human-approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --source-dry-run-review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --runtime-config-target "$TMP_ROOT/controlled_runtime_calibration_applied_runtime_config_v1.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-application-execution-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution-inputs "$TMP_ROOT/controlled_runtime_calibration_application_execution_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli execute-controlled-runtime-calibration-application \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution-inputs "$TMP_ROOT/controlled_runtime_calibration_application_execution_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --rollback-package-output "$TMP_ROOT/controlled_runtime_calibration_application_rollback_package.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-application-execution \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli verify-controlled-runtime-calibration-runtime-readback \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --runtime-config-target "$TMP_ROOT/controlled_runtime_calibration_applied_runtime_config_v1.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_runtime_readback.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-application-audit-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_audit_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-rollback-package \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_rollback_package.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-post-apply-verification-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --application-execution "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_post_apply_verification.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli export-controlled-runtime-calibration-application-execution-review-packet-contract \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-application-execution-review-packet-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --source-application-execution "$TMP_ROOT/controlled_runtime_calibration_application_execution.current.json" \
  --source-application-execution-contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_contract_v1.smoke.json" \
  --source-runtime-config-artifact "$TMP_ROOT/controlled_runtime_calibration_applied_runtime_config_v1.json" \
  --source-rollback-package "$TMP_ROOT/controlled_runtime_calibration_application_rollback_package.current.json" \
  --source-pre-application-final-gate "$TMP_ROOT/controlled_runtime_calibration_pre_application_final_gate.current.json" \
  --source-runtime-application-staging "$TMP_ROOT/controlled_runtime_calibration_runtime_application_staging.current.json" \
  --source-application-plan "$TMP_ROOT/controlled_runtime_calibration_application_plan.current.json" \
  --source-human-approval-gate "$TMP_ROOT/controlled_runtime_calibration_human_approval_gate.current.json" \
  --source-dry-run-review-packet "$TMP_ROOT/controlled_runtime_calibration_dry_run_review_packet.current.json" \
  --source-dry-run-execution-report "$TMP_ROOT/controlled_runtime_calibration_dry_run_execution.current.json" \
  --source-change-request "$TMP_ROOT/controlled_runtime_calibration_change_request.current.json" \
  --source-candidate-config-freeze "$TMP_ROOT/calibration_candidate_config_freeze.current.json" \
  --source-manual-approval-packet "$TMP_ROOT/calibration_candidate_manual_approval_packet.current.json" \
  --source-decision-packet "$TMP_ROOT/calibration_candidate_decision_packet.current.json" \
  --source-phase-freeze "$TMP_ROOT/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.smoke.json" \
  --source-gameplay-gate-regression-baseline "$TMP_ROOT/gameplay_gate_regression.baseline.json" \
  --source-calibration-sandbox-baseline "$TMP_ROOT/review_guided_gameplay_calibration_sandbox.baseline.json" \
  --model-asset-path "model_assets/tom_v1/view_classifier_gameplay.pt" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_inputs.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-application-execution-review-packet-inputs \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet-inputs "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_inputs.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-application-execution-review-packet \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet-inputs "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_inputs.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli validate-controlled-runtime-calibration-application-execution-review-packet \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.validation.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-post-execution-summary \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_post_execution_summary.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-post-execution-blocker-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_post_execution_blocker_report.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-post-execution-operator-checklist \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_post_execution_operator_checklist.current.json" \
  --skip-create-db

run "$PYTHON_BIN" -m apps.worker.cli build-controlled-runtime-calibration-post-execution-next-action-report \
  --contract "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet_contract_v1.smoke.json" \
  --review-packet "$TMP_ROOT/controlled_runtime_calibration_application_execution_review_packet.current.json" \
  --output "$TMP_ROOT/controlled_runtime_calibration_post_execution_next_action_report.current.json" \
  --skip-create-db

run git status --short
