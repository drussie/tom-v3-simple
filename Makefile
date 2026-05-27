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
MAX_GAP_FRAMES ?= 30
TRACKLET_ID ?=
QUERY_JSON ?=
EXPORT_ROOT ?= .data/exports
YOLO_DEVICE ?= auto
WEIGHTS_PATH ?=
MODEL_NAME ?=
MODEL_VERSION ?= v0
REQUIRED_SHA256 ?=
RUN_TRACKLETS ?= false
SOURCE_DETECTION_RUN_ID ?=
LINK_SOURCE_DETECTIONS ?= false
DEMO_MEDIA_PATH ?=
VIEWER_BASE_URL ?= http://127.0.0.1:3000
TRACKLET_RUN_ID ?=
POSE_RUN_ID ?=
AUDIT_DEMO_ONLY ?= true
AUDIT_STRICT ?= false
TOM_V3_AUDIT_REQUIRED ?= false

export TOM_V3_DATABASE_URL

.PHONY: install web-install test lint migrate api seed verify index-media run-gameplay index-and-run-gameplay run-detection index-and-run-detection extract-frame-artifacts build-tracklets run-pose export-tracklet-review-dataset demo demo-fixture demo-plan demo-reset demo-export demo-open replay-open completion-audit completion-check yolo-probe yolo-smoke yolo-runtime-probe register-yolo-model smoke-real-yolo-local web web-build web-lint smoke all-checks

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
	$(PYTHON) -m apps.worker.cli build-tracklets --detection-run-id "$(DETECTION_RUN_ID)" --max-gap-frames "$(MAX_GAP_FRAMES)"

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
	else \
		echo "$(VIEWER_BASE_URL)/replay/$(MEDIA_ID)"; \
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
