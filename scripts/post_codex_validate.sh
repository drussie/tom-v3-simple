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

run git status --short
