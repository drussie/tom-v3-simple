PYTHON ?= python
WEB_DIR := apps/web
TOM_V3_DATABASE_URL ?= sqlite+pysqlite:///./tmp_tom_v3.db
RUN_ID ?=
MEDIA_ID ?=
SOURCE_PATH ?=
STORAGE_ROOT ?= .data/media
ADAPTER ?= fixture
FRAME_SAMPLE_RATE ?= 30
MAX_FRAMES ?= 5
ARTIFACT_ROOT ?= .data/artifacts
DETECTION_RUN_ID ?=
RUN_NAME ?= tracklet-builder-run
MAX_GAP_FRAMES ?= 30
TRACKLET_ID ?=
QUERY_JSON ?=
EXPORT_ROOT ?= .data/exports
YOLO_DEVICE ?= auto
WEIGHTS_PATH ?=
YOLO_WEIGHTS_PATH ?= $(WEIGHTS_PATH)
POSE_WEIGHTS_PATH ?= $(WEIGHTS_PATH)
TOM_V1_MODEL_ROOT ?= model_assets/tom_v1
TOM_V1_BALL_CONF ?= 0.10
TOM_V1_PLAYER_CONF ?= 0.25
TOM_V1_POSE_CONF ?= 0.25
TOM_V1_COURT_KEYPOINT_IMG_SIZE ?= 224
COURT_KEYPOINT_PREPROCESSING_MODE ?= full_frame_resize_224
COURT_KEYPOINT_COORDINATE_INTERPRETATION ?= output_as_pixels_224
EMIT_DEBUG_ARTIFACTS ?= false
MODEL_NAME ?=
MODEL_VERSION ?= v0
REQUIRED_SHA256 ?=
RUN_TRACKLETS ?= false
SOURCE_DETECTION_RUN_ID ?=
SOURCE_SUBJECT_RUN_ID ?=
SOURCE_TRACK_RUN_ID ?=
MAIN_PLAYER_TRACK_RUN_ID ?=
LINK_SOURCE_DETECTIONS ?= false
DEMO_MEDIA_PATH ?=
VIEWER_BASE_URL ?= http://127.0.0.1:3000
TRACKLET_RUN_ID ?=
POSE_RUN_ID ?=
MOTION_SMOOTHING_RUN_ID ?=
COURT_PROJECTION_RUN_NAME ?= object-to-court-projection-candidates-v0
COURT_PROJECTION_RUN_ID ?=
BALL_TRAJECTORY_RUN_NAME ?= ball-trajectory-court-candidate-v0
BALL_TRAJECTORY_RUN_ID ?=
EVENT_CANDIDATE_RUN_NAME ?= hit-bounce-candidate-evidence-v0
EVENT_CANDIDATE_RUN_ID ?=
HOMOGRAPHY_MAX_GAP_MS ?= 1500
BALL_TRAJECTORY_MAX_GAP_FRAMES ?= 6
BALL_TRAJECTORY_MAX_GAP_MS ?= 250
BALL_TRAJECTORY_MIN_POINTS_PER_SEGMENT ?= 3
HIT_PLAYER_DISTANCE_MAX_TEMPLATE ?= 0.18
BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE ?= 0.18
HIT_MIN_DIRECTION_DELTA_DEGREES ?= 25
BOUNCE_MIN_DIRECTION_DELTA_DEGREES ?= 20
HIT_MIN_NET_AXIS_DELTA_TEMPLATE ?= 0.015
BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS ?= 2.0
BOUNCE_MIN_SPEED_REDUCTION_FRACTION ?= 0.05
HIT_PLAYER_TIME_WINDOW_MS ?= 300
HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION ?= 0.45
HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES ?= 5.0
BOUNCE_FALLBACK_ENABLED ?= true
BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION ?= 0.35
PLAYER_ANCHORED_HIT_ENABLED ?= true
PLAYER_ANCHORED_HIT_LOOKBACK_MS ?= 700
PLAYER_ANCHORED_HIT_LOOKAHEAD_MS ?= 1300
PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE ?= 0.24
PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE ?= 0.015
PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS ?= 60
EVENT_OVERLAP_DISTANCE_TEMPLATE ?= 0.08
CANDIDATE_DEDUPE_MS ?= 500
AUDIT_DEMO_ONLY ?= true
AUDIT_STRICT ?= false
TOM_V3_AUDIT_REQUIRED ?= false
EVERY_N_FRAMES ?= 1
IMG_SIZE ?=
CONF ?= 0.25
IOU ?= 0.7
FRAME_START ?=
FRAME_END ?=
CLASS_MAP_JSON ?=
PLAN_ONLY ?= false
OUTPUT_DEBUG_ARTIFACT ?= false
POSE_MODE ?= crop_from_player_detection
FALLBACK_TO_FULL_FRAME ?= false
COURT_RUN_NAME ?= fixture-court-evidence
COURT_RUN_ID ?=
HOMOGRAPHY_RUN_NAME ?= homography-candidate-builder
HOMOGRAPHY_RUN_ID ?=
PROJECTION_DIAGNOSTIC_RUN_NAME ?= projection-diagnostic-builder
PROJECTION_DIAGNOSTIC_RUN_ID ?=
MIN_KEYPOINT_CONFIDENCE ?= 0.0
DERIVE_LINES ?= true

export TOM_V3_DATABASE_URL

.PHONY: install web-install test lint migrate api seed verify index-media run-gameplay index-and-run-gameplay run-detection index-and-run-detection extract-frame-artifacts build-tracklets run-pose export-tracklet-review-dataset court-review-export demo demo-fixture demo-plan demo-reset demo-export demo-open replay-open completion-audit completion-check yolo-probe yolo-smoke yolo-runtime-probe register-yolo-model smoke-real-yolo-local real-detection real-pose tom-v1-yolo-probe tom-v1-ball-detection tom-v1-player-detection tom-v1-tracklets tom-v1-main-subjects tom-v1-main-player-tracks tom-v1-pose tom-v1-pose-main-subjects tom-v1-pose-main-tracks tom-v1-motion-smoothing tom-v1-court-keypoints-probe tom-v1-court-keypoints tom-v1-court-keypoint-audit tom-v1-object-court-projection tom-v1-ball-court-trajectory tom-v1-hit-bounce-candidates court-fixture homography-candidates projection-diagnostics web web-build web-lint smoke all-checks

install:
	$(PYTHON) -m pip install -e ".[dev]"

web-install:
	cd $(WEB_DIR) && npm install

test:
	$(PYTHON) -m pytest -q

lint:
	ruff check .

migrate:
	alembic upgrade head

api:
	uvicorn apps.api.main:app --reload

seed:
	$(PYTHON) -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip --source-uri file:///dev/synthetic-tennis-clip.mp4 --run-name synthetic-baseline-run

verify:
	@if [ -z "$(RUN_ID)" ]; then echo "RUN_ID is required: make verify RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli verify-synthetic-run --run-id $(RUN_ID)

index-media:
	@if [ -z "$(SOURCE_PATH)" ]; then echo "SOURCE_PATH is required: make index-media SOURCE_PATH=/path/to/video.mp4"; exit 1; fi
	$(PYTHON) -m apps.worker.cli index-media --source-path "$(SOURCE_PATH)" --storage-root "$(STORAGE_ROOT)"

run-gameplay:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make run-gameplay MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-gameplay-adapter --media-id "$(MEDIA_ID)" --adapter "$(ADAPTER)"

index-and-run-gameplay:
	@if [ -z "$(SOURCE_PATH)" ]; then echo "SOURCE_PATH is required: make index-and-run-gameplay SOURCE_PATH=/path/to/video.mp4"; exit 1; fi
	$(PYTHON) -m apps.worker.cli index-and-run-gameplay --source-path "$(SOURCE_PATH)" --storage-root "$(STORAGE_ROOT)" --adapter "$(ADAPTER)"

run-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make run-detection MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-detection-adapter --media-id "$(MEDIA_ID)" --adapter "$(ADAPTER)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)"

index-and-run-detection:
	@if [ -z "$(SOURCE_PATH)" ]; then echo "SOURCE_PATH is required: make index-and-run-detection SOURCE_PATH=/path/to/video.mp4"; exit 1; fi
	$(PYTHON) -m apps.worker.cli index-and-run-detection --source-path "$(SOURCE_PATH)" --storage-root "$(STORAGE_ROOT)" --adapter "$(ADAPTER)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)"

extract-frame-artifacts:
	@if [ -z "$(RUN_ID)" ]; then echo "RUN_ID is required: make extract-frame-artifacts RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli extract-frame-artifacts --run-id "$(RUN_ID)" --max-frames "$(MAX_FRAMES)" --output-root "$(ARTIFACT_ROOT)"

build-tracklets:
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make build-tracklets DETECTION_RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-tracklets --detection-run-id "$(DETECTION_RUN_ID)" --run-name "$(RUN_NAME)" --max-gap-frames "$(MAX_GAP_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

run-pose:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make run-pose MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-pose-adapter --media-id "$(MEDIA_ID)" --adapter fixture --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" $(if $(SOURCE_DETECTION_RUN_ID),--source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)",) $(if $(filter true,$(LINK_SOURCE_DETECTIONS)),--link-source-detections,--no-link-source-detections)

export-tracklet-review-dataset:
	@if [ -z "$(TRACKLET_ID)" ] && [ -z "$(QUERY_JSON)" ]; then echo "TRACKLET_ID or QUERY_JSON is required"; exit 1; fi
	@if [ -n "$(TRACKLET_ID)" ]; then $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --tracklet-id "$(TRACKLET_ID)" --output-root "$(EXPORT_ROOT)"; else $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --query-json '$(QUERY_JSON)' --output-root "$(EXPORT_ROOT)"; fi

demo:
	$(PYTHON) -m apps.worker.cli run-demo $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",$(if $(DEMO_MEDIA_PATH),--source-path "$(DEMO_MEDIA_PATH)",)) --storage-root "$(STORAGE_ROOT)" --artifact-root "$(ARTIFACT_ROOT)" --export-root "$(EXPORT_ROOT)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

demo-fixture:
	$(PYTHON) -m apps.worker.cli run-demo $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",$(if $(DEMO_MEDIA_PATH),--source-path "$(DEMO_MEDIA_PATH)",)) --storage-root "$(STORAGE_ROOT)" --artifact-root "$(ARTIFACT_ROOT)" --export-root "$(EXPORT_ROOT)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

demo-plan:
	$(PYTHON) -m apps.worker.cli run-demo --plan-only $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",$(if $(DEMO_MEDIA_PATH),--source-path "$(DEMO_MEDIA_PATH)",)) --storage-root "$(STORAGE_ROOT)" --artifact-root "$(ARTIFACT_ROOT)" --export-root "$(EXPORT_ROOT)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

demo-reset:
	@echo "demo-reset is intentionally non-destructive. TOM v3 demo runs are additive."; \
	echo "To start fresh, set TOM_V3_DATABASE_URL to a new SQLite file, for example:"; \
	echo "  TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo.db make demo"; \
	echo "Local demo outputs live under .data/demo, $(ARTIFACT_ROOT), and $(EXPORT_ROOT). Remove only files you intentionally created."

demo-export:
	@if [ -z "$(RUN_ID)" ] && [ -z "$(TRACKLET_ID)" ] && [ -z "$(QUERY_JSON)" ]; then echo "RUN_ID for pose export or TRACKLET_ID/QUERY_JSON for tracklet export is required."; exit 1; fi
	@if [ -n "$(RUN_ID)" ]; then $(PYTHON) -m apps.worker.cli export-pose-review-dataset --run-id "$(RUN_ID)" --output-root "$(EXPORT_ROOT)" --created-by tom-v3-demo; fi
	@if [ -n "$(TRACKLET_ID)" ]; then $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --tracklet-id "$(TRACKLET_ID)" --output-root "$(EXPORT_ROOT)" --created-by tom-v3-demo; fi
	@if [ -n "$(QUERY_JSON)" ]; then $(PYTHON) -m apps.worker.cli export-tracklet-review-dataset --query-json '$(QUERY_JSON)' --output-root "$(EXPORT_ROOT)" --created-by tom-v3-demo; fi

demo-open:
	@echo "Open viewer URLs manually:"; \
	if [ -n "$(RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(RUN_ID)"; fi; \
	if [ -n "$(DETECTION_RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(DETECTION_RUN_ID)"; fi; \
	if [ -n "$(TRACKLET_RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(TRACKLET_RUN_ID)"; fi; \
	if [ -n "$(POSE_RUN_ID)" ]; then echo "$(VIEWER_BASE_URL)/runs/$(POSE_RUN_ID)"; fi; \
	if [ -z "$(RUN_ID)" ] && [ -z "$(DETECTION_RUN_ID)" ] && [ -z "$(TRACKLET_RUN_ID)" ] && [ -z "$(POSE_RUN_ID)" ]; then echo "Pass RUN_ID=<run_id>, DETECTION_RUN_ID=<run_id>, TRACKLET_RUN_ID=<run_id>, or POSE_RUN_ID=<run_id>."; fi

replay-open:
	@if [ -z "$(MEDIA_ID)" ]; then \
		echo "Pass MEDIA_ID=<media_id>, then open:"; \
		echo "  $(VIEWER_BASE_URL)/replay/<media_id>"; \
		echo "Optional: MODE=stream_proxy DETECTION_RUN_ID=<run_id> TRACKLET_RUN_ID=<run_id> POSE_RUN_ID=<run_id>"; \
	else \
		url="$(VIEWER_BASE_URL)/replay/$(MEDIA_ID)"; sep="?"; \
		if [ -n "$(MODE)" ]; then url="$$url$${sep}mode=$(MODE)"; sep="&"; fi; \
		if [ -n "$(DETECTION_RUN_ID)" ]; then url="$$url$${sep}detectionRunId=$(DETECTION_RUN_ID)"; sep="&"; fi; \
		if [ -n "$(TRACKLET_RUN_ID)" ]; then url="$$url$${sep}trackletRunId=$(TRACKLET_RUN_ID)"; sep="&"; fi; \
		if [ -n "$(POSE_RUN_ID)" ]; then url="$$url$${sep}poseRunId=$(POSE_RUN_ID)"; sep="&"; fi; \
		echo "$$url"; \
	fi

completion-audit:
	$(PYTHON) -m apps.worker.cli completion-audit $(if $(MEDIA_ID),--media-id "$(MEDIA_ID)",) $(if $(filter false,$(AUDIT_DEMO_ONLY)),--no-demo-only,--demo-only) $(if $(filter true,$(AUDIT_STRICT)),--strict,--no-strict)

completion-check:
	$(PYTHON) -m pytest -q
	ruff check .
	$(PYTHON) scripts/smoke_synthetic_viewer_data.py
	@if [ "$(TOM_V3_AUDIT_REQUIRED)" = "true" ]; then \
		$(PYTHON) -m apps.worker.cli completion-audit --demo-only; \
	else \
		echo "Run make demo then make completion-audit for the full provenance audit."; \
	fi

yolo-probe: yolo-runtime-probe

yolo-smoke:
	$(PYTHON) -m apps.worker.cli smoke-real-yolo-local --plan-only $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",) $(if $(WEIGHTS_PATH),--weights-path "$(WEIGHTS_PATH)",) $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" --device "$(YOLO_DEVICE)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --output-root "$(ARTIFACT_ROOT)" $(if $(filter true,$(RUN_TRACKLETS)),--run-tracklets,--no-run-tracklets)

yolo-runtime-probe:
	$(PYTHON) -m apps.worker.cli yolo-runtime-probe --device "$(YOLO_DEVICE)"

register-yolo-model:
	@if [ -z "$(WEIGHTS_PATH)" ]; then echo "WEIGHTS_PATH is required: make register-yolo-model WEIGHTS_PATH=model_assets/yolo/model.pt"; exit 1; fi
	$(PYTHON) -m apps.worker.cli register-yolo-model --weights-path "$(WEIGHTS_PATH)" --model-version "$(MODEL_VERSION)" $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) $(if $(REQUIRED_SHA256),--required-sha256 "$(REQUIRED_SHA256)",)

smoke-real-yolo-local:
	$(PYTHON) -m apps.worker.cli smoke-real-yolo-local $(if $(SOURCE_PATH),--source-path "$(SOURCE_PATH)",) $(if $(WEIGHTS_PATH),--weights-path "$(WEIGHTS_PATH)",) $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" --device "$(YOLO_DEVICE)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --output-root "$(ARTIFACT_ROOT)" $(if $(filter true,$(RUN_TRACKLETS)),--run-tracklets,--no-run-tracklets)

real-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=model_assets/yolo/model.pt"; exit 1; fi
	@if [ -z "$(YOLO_WEIGHTS_PATH)" ]; then echo "YOLO_WEIGHTS_PATH is required: make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=model_assets/yolo/model.pt"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-detection --media-id "$(MEDIA_ID)" --weights "$(YOLO_WEIGHTS_PATH)" --device "$(YOLO_DEVICE)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" $(if $(REQUIRED_SHA256),--required-sha256 "$(REQUIRED_SHA256)",) $(if $(IMG_SIZE),--imgsz "$(IMG_SIZE)",) $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(CLASS_MAP_JSON),--class-map-json '$(CLASS_MAP_JSON)',) $(if $(filter true,$(OUTPUT_DEBUG_ARTIFACT)),--output-debug-artifact,--no-output-debug-artifact) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

real-pose:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make real-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<run_id> POSE_WEIGHTS_PATH=model_assets/pose/model.pt"; exit 1; fi
	@if [ -z "$(POSE_WEIGHTS_PATH)" ]; then echo "POSE_WEIGHTS_PATH is required: make real-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<run_id> POSE_WEIGHTS_PATH=model_assets/pose/model.pt"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --weights "$(POSE_WEIGHTS_PATH)" $(if $(SOURCE_DETECTION_RUN_ID),--source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)",) $(if $(SOURCE_SUBJECT_RUN_ID),--source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)",) $(if $(SOURCE_TRACK_RUN_ID),--source-track-run-id "$(SOURCE_TRACK_RUN_ID)",) --mode "$(POSE_MODE)" --device "$(YOLO_DEVICE)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(MODEL_NAME),--model-name "$(MODEL_NAME)",) --model-version "$(MODEL_VERSION)" $(if $(REQUIRED_SHA256),--required-sha256 "$(REQUIRED_SHA256)",) $(if $(IMG_SIZE),--imgsz "$(IMG_SIZE)",) $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-yolo-probe:
	$(PYTHON) -m apps.worker.cli yolo-runtime-probe --device "$(YOLO_DEVICE)"

tom-v1-ball-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-ball-detection MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-detection --media-id "$(MEDIA_ID)" --weights "$(TOM_V1_MODEL_ROOT)/best_ball_v2_1280.pt" --model-name tom-v1-best-ball-v2-1280 --model-version v1-local --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),1280)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_BALL_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(CLASS_MAP_JSON),--class-map-json '$(CLASS_MAP_JSON)',) $(if $(filter true,$(OUTPUT_DEBUG_ARTIFACT)),--output-debug-artifact,--no-output-debug-artifact) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-player-detection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-player-detection MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-detection --media-id "$(MEDIA_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x.pt" --model-name tom-v1-yolo26x-player-detector --model-version v1-local --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_PLAYER_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(CLASS_MAP_JSON),--class-map-json '$(CLASS_MAP_JSON)',) $(if $(filter true,$(OUTPUT_DEBUG_ARTIFACT)),--output-debug-artifact,--no-output-debug-artifact) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-tracklets:
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make tom-v1-tracklets DETECTION_RUN_ID=<run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-tracklets --detection-run-id "$(DETECTION_RUN_ID)" --run-name tom-v1-model-derived-tracklets --max-gap-frames "$(MAX_GAP_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)"

tom-v1-main-subjects:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-main-subjects MEDIA_ID=<media_id> DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make tom-v1-main-subjects DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli select-main-player-subjects --media-id "$(MEDIA_ID)" --source-detection-run-id "$(DETECTION_RUN_ID)" --run-name main-player-subject-filter-v0 --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-main-player-tracks:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-main-player-tracks MEDIA_ID=<media_id> DETECTION_RUN_ID=<player_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	@if [ -z "$(DETECTION_RUN_ID)" ]; then echo "DETECTION_RUN_ID is required: make tom-v1-main-player-tracks DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_SUBJECT_RUN_ID)" ]; then echo "SOURCE_SUBJECT_RUN_ID is required: make tom-v1-main-player-tracks SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli assign-main-player-tracks --media-id "$(MEDIA_ID)" --source-detection-run-id "$(DETECTION_RUN_ID)" --source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)" --run-name main-player-track-assignment-v01 --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-pose:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_DETECTION_RUN_ID)" ]; then echo "SOURCE_DETECTION_RUN_ID is required: make tom-v1-pose SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt" --model-name tom-v1-yolo26x-pose --model-version v1-local --mode crop_from_player_detection --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_POSE_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-pose-main-subjects:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-pose-main-subjects MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_DETECTION_RUN_ID)" ]; then echo "SOURCE_DETECTION_RUN_ID is required: make tom-v1-pose-main-subjects SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_SUBJECT_RUN_ID)" ]; then echo "SOURCE_SUBJECT_RUN_ID is required: make tom-v1-pose-main-subjects SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)" --source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt" --model-name tom-v1-yolo26x-pose --model-version v1-local --mode crop_from_player_detection --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_POSE_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-pose-main-tracks:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-pose-main-tracks MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> SOURCE_TRACK_RUN_ID=<main_player_track_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_DETECTION_RUN_ID)" ]; then echo "SOURCE_DETECTION_RUN_ID is required: make tom-v1-pose-main-tracks SOURCE_DETECTION_RUN_ID=<player_detection_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_SUBJECT_RUN_ID)" ]; then echo "SOURCE_SUBJECT_RUN_ID is required: make tom-v1-pose-main-tracks SOURCE_SUBJECT_RUN_ID=<main_subject_run_id>"; exit 1; fi
	@if [ -z "$(SOURCE_TRACK_RUN_ID)" ]; then echo "SOURCE_TRACK_RUN_ID is required: make tom-v1-pose-main-tracks SOURCE_TRACK_RUN_ID=<main_player_track_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-pose --media-id "$(MEDIA_ID)" --source-detection-run-id "$(SOURCE_DETECTION_RUN_ID)" --source-subject-run-id "$(SOURCE_SUBJECT_RUN_ID)" --source-track-run-id "$(SOURCE_TRACK_RUN_ID)" --weights "$(TOM_V1_MODEL_ROOT)/yolo26x-pose.pt" --model-name tom-v1-yolo26x-pose --model-version v1-local --mode crop_from_player_detection --device "$(YOLO_DEVICE)" --imgsz "$(if $(IMG_SIZE),$(IMG_SIZE),640)" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --conf "$(TOM_V1_POSE_CONF)" --iou "$(IOU)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(FALLBACK_TO_FULL_FRAME)),--fallback-to-full-frame,--no-fallback-to-full-frame) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-motion-smoothing:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-motion-smoothing MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli smooth-motion-candidates --media-id "$(MEDIA_ID)" $(if $(DETECTION_RUN_ID),--detection-run-id "$(DETECTION_RUN_ID)",) $(if $(TRACKLET_RUN_ID),--tracklet-run-id "$(TRACKLET_RUN_ID)",) $(if $(MAIN_PLAYER_TRACK_RUN_ID),--main-player-track-run-id "$(MAIN_PLAYER_TRACK_RUN_ID)",) $(if $(POSE_RUN_ID),--pose-run-id "$(POSE_RUN_ID)",) --run-name motion-smoothing-stable-replay-candidates-v0 --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-object-court-projection:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-object-court-projection MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(MOTION_SMOOTHING_RUN_ID)" ]; then echo "MOTION_SMOOTHING_RUN_ID is required: make tom-v1-object-court-projection MOTION_SMOOTHING_RUN_ID=<motion_smoothing_run_id>"; exit 1; fi
	@if [ -z "$(HOMOGRAPHY_RUN_ID)" ]; then echo "HOMOGRAPHY_RUN_ID is required: make tom-v1-object-court-projection HOMOGRAPHY_RUN_ID=<homography_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli project-objects-to-court --media-id "$(MEDIA_ID)" --motion-smoothing-run-id "$(MOTION_SMOOTHING_RUN_ID)" --homography-run-id "$(HOMOGRAPHY_RUN_ID)" --run-name "$(COURT_PROJECTION_RUN_NAME)" --homography-max-gap-ms "$(HOMOGRAPHY_MAX_GAP_MS)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-ball-court-trajectory:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-ball-court-trajectory MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(COURT_PROJECTION_RUN_ID)" ]; then echo "COURT_PROJECTION_RUN_ID is required: make tom-v1-ball-court-trajectory COURT_PROJECTION_RUN_ID=<court_projection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-ball-court-trajectory --media-id "$(MEDIA_ID)" --court-projection-run-id "$(COURT_PROJECTION_RUN_ID)" --run-name "$(BALL_TRAJECTORY_RUN_NAME)" --max-gap-frames "$(BALL_TRAJECTORY_MAX_GAP_FRAMES)" --max-gap-ms "$(BALL_TRAJECTORY_MAX_GAP_MS)" --min-points-per-segment "$(BALL_TRAJECTORY_MIN_POINTS_PER_SEGMENT)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-hit-bounce-candidates:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-hit-bounce-candidates MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(BALL_TRAJECTORY_RUN_ID)" ]; then echo "BALL_TRAJECTORY_RUN_ID is required: make tom-v1-hit-bounce-candidates BALL_TRAJECTORY_RUN_ID=<ball_trajectory_run_id>"; exit 1; fi
	@if [ -z "$(COURT_PROJECTION_RUN_ID)" ]; then echo "COURT_PROJECTION_RUN_ID is required: make tom-v1-hit-bounce-candidates COURT_PROJECTION_RUN_ID=<court_projection_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-hit-bounce-candidates --media-id "$(MEDIA_ID)" --ball-trajectory-run-id "$(BALL_TRAJECTORY_RUN_ID)" --court-projection-run-id "$(COURT_PROJECTION_RUN_ID)" --run-name "$(EVENT_CANDIDATE_RUN_NAME)" --hit-player-distance-max-template "$(HIT_PLAYER_DISTANCE_MAX_TEMPLATE)" --bounce-player-distance-min-template "$(BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE)" --hit-min-direction-delta-degrees "$(HIT_MIN_DIRECTION_DELTA_DEGREES)" --bounce-min-direction-delta-degrees "$(BOUNCE_MIN_DIRECTION_DELTA_DEGREES)" --hit-min-net-axis-delta-template "$(HIT_MIN_NET_AXIS_DELTA_TEMPLATE)" --bounce-min-image-y-delta-pixels "$(BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS)" --bounce-min-speed-reduction-fraction "$(BOUNCE_MIN_SPEED_REDUCTION_FRACTION)" --hit-player-time-window-ms "$(HIT_PLAYER_TIME_WINDOW_MS)" --hit-contact-fallback-min-speed-delta-fraction "$(HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION)" --hit-contact-fallback-min-direction-delta-degrees "$(HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES)" $(if $(filter false,$(BOUNCE_FALLBACK_ENABLED)),--no-bounce-fallback-enabled,--bounce-fallback-enabled) --bounce-fallback-min-speed-reduction-fraction "$(BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION)" $(if $(filter false,$(PLAYER_ANCHORED_HIT_ENABLED)),--no-player-anchored-hit-enabled,--player-anchored-hit-enabled) --player-anchored-hit-lookback-ms "$(PLAYER_ANCHORED_HIT_LOOKBACK_MS)" --player-anchored-hit-lookahead-ms "$(PLAYER_ANCHORED_HIT_LOOKAHEAD_MS)" --player-anchored-hit-distance-max-template "$(PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE)" --player-anchored-hit-min-net-axis-delta-template "$(PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE)" --player-anchored-hit-min-pre-post-gap-ms "$(PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS)" --event-overlap-distance-template "$(EVENT_OVERLAP_DISTANCE_TEMPLATE)" --candidate-dedupe-ms "$(CANDIDATE_DEDUPE_MS)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-court-keypoints-probe:
	$(PYTHON) -m apps.worker.cli tom-v1-court-keypoints-probe --weights "$(TOM_V1_MODEL_ROOT)/keypoints_model.pth" --allowed-root "$(TOM_V1_MODEL_ROOT)"

tom-v1-court-keypoints:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-court-keypoints MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-real-court-keypoints --media-id "$(MEDIA_ID)" --weights "$(TOM_V1_MODEL_ROOT)/keypoints_model.pth" --model-name tom-v1-court-keypoints --model-version v1-local --device "$(YOLO_DEVICE)" --img-size "$(if $(IMG_SIZE),$(IMG_SIZE),$(TOM_V1_COURT_KEYPOINT_IMG_SIZE))" --every-n-frames "$(EVERY_N_FRAMES)" --max-frames "$(MAX_FRAMES)" --viewer-base-url "$(VIEWER_BASE_URL)" --allowed-root "$(TOM_V1_MODEL_ROOT)" --preprocessing-mode "$(COURT_KEYPOINT_PREPROCESSING_MODE)" --coordinate-interpretation "$(COURT_KEYPOINT_COORDINATE_INTERPRETATION)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter false,$(DERIVE_LINES)),--no-derive-lines,--derive-lines) $(if $(filter true,$(EMIT_DEBUG_ARTIFACTS)),--emit-debug-artifacts,) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

tom-v1-court-keypoint-audit:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make tom-v1-court-keypoint-audit MEDIA_ID=<media_id>"; exit 1; fi
	$(MAKE) tom-v1-court-keypoints MEDIA_ID="$(MEDIA_ID)" PYTHON="$(PYTHON)" YOLO_DEVICE="$(YOLO_DEVICE)" IMG_SIZE="$(if $(IMG_SIZE),$(IMG_SIZE),224)" EVERY_N_FRAMES="$(EVERY_N_FRAMES)" MAX_FRAMES="$(MAX_FRAMES)" VIEWER_BASE_URL="$(VIEWER_BASE_URL)" COURT_KEYPOINT_PREPROCESSING_MODE="$(COURT_KEYPOINT_PREPROCESSING_MODE)" COURT_KEYPOINT_COORDINATE_INTERPRETATION="$(COURT_KEYPOINT_COORDINATE_INTERPRETATION)" EMIT_DEBUG_ARTIFACTS=true DERIVE_LINES="$(DERIVE_LINES)" PLAN_ONLY="$(PLAN_ONLY)"

court-fixture:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make court-fixture MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli run-fixture-court --media-id "$(MEDIA_ID)" --frame-sample-rate "$(FRAME_SAMPLE_RATE)" --max-frames "$(MAX_FRAMES)" --run-name "$(COURT_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

homography-candidates:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make homography-candidates MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(COURT_RUN_ID)" ]; then echo "COURT_RUN_ID is required: make homography-candidates COURT_RUN_ID=<court_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-homography-candidates --media-id "$(MEDIA_ID)" --court-run-id "$(COURT_RUN_ID)" --run-name "$(HOMOGRAPHY_RUN_NAME)" --min-keypoint-confidence "$(MIN_KEYPOINT_CONFIDENCE)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

projection-diagnostics:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make projection-diagnostics MEDIA_ID=<media_id>"; exit 1; fi
	@if [ -z "$(HOMOGRAPHY_RUN_ID)" ]; then echo "HOMOGRAPHY_RUN_ID is required: make projection-diagnostics HOMOGRAPHY_RUN_ID=<homography_run_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli build-projection-diagnostics --media-id "$(MEDIA_ID)" --homography-run-id "$(HOMOGRAPHY_RUN_ID)" --run-name "$(PROJECTION_DIAGNOSTIC_RUN_NAME)" --viewer-base-url "$(VIEWER_BASE_URL)" $(if $(FRAME_START),--frame-start "$(FRAME_START)",) $(if $(FRAME_END),--frame-end "$(FRAME_END)",) $(if $(filter true,$(PLAN_ONLY)),--plan-only,)

court-review-export:
	@if [ -z "$(MEDIA_ID)" ]; then echo "MEDIA_ID is required: make court-review-export MEDIA_ID=<media_id>"; exit 1; fi
	$(PYTHON) -m apps.worker.cli export-court-review-dataset --media-id "$(MEDIA_ID)" $(if $(COURT_RUN_ID),--court-run-id "$(COURT_RUN_ID)",) $(if $(HOMOGRAPHY_RUN_ID),--homography-run-id "$(HOMOGRAPHY_RUN_ID)",) $(if $(PROJECTION_DIAGNOSTIC_RUN_ID),--projection-diagnostic-run-id "$(PROJECTION_DIAGNOSTIC_RUN_ID)",) --output-root "$(EXPORT_ROOT)"

web:
	cd $(WEB_DIR) && npm run dev

web-build:
	cd $(WEB_DIR) && npm run build

web-lint:
	cd $(WEB_DIR) && npm run lint

smoke:
	$(PYTHON) scripts/smoke_synthetic_viewer_data.py

all-checks:
	$(PYTHON) -m pytest -q
	ruff check .
	cd $(WEB_DIR) && npm run lint
	cd $(WEB_DIR) && npm run build
