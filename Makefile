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

export TOM_V3_DATABASE_URL

.PHONY: install web-install test lint migrate api seed verify index-media run-gameplay index-and-run-gameplay run-detection index-and-run-detection extract-frame-artifacts web web-build web-lint smoke all-checks

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
