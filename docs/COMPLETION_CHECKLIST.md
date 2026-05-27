# TOM v3 Simple Completion Checklist

Use this checklist for final local validation and completion review.

## Demo Checklist

Run:

```bash
make demo
```

Expected:

- media is indexed or generated
- fixture gameplay run is created
- fixture detection run is created
- frame artifacts are extracted
- candidate tracklets are built
- fixture pose run is created
- review annotations are seeded
- pose and tracklet review exports are written
- viewer URLs are printed

Optional custom media:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
```

Local video files under `demo_assets/` should not be committed unless intentionally tracked.

## Viewer Checklist

Start local services:

```bash
uvicorn apps.api.main:app --reload
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/runs/<run_id>
```

Confirm:

- detection observations appear
- detection bboxes render when bbox payloads exist
- frame artifacts display when available
- tracklet candidates and track point candidates appear
- lineage is readable
- pose observations render keypoint evidence
- missing keypoints stay missing
- annotations are visible
- review export artifacts appear when present in the run payload

## Provenance Audit Checklist

After `make demo`, run:

```bash
make completion-audit
```

Expected:

- `ok = true`
- `status = passed`
- media/run/step/observation/typed-row/lineage/artifact/annotation/export checks pass

For custom media DB:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point.db \
make completion-audit PYTHON=.venv/bin/python
```

## Docs Checklist

Confirm these files exist and are current:

- `README.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/CONTROL_ROOM.md`
- `docs/ARCHITECTURE.md`
- `docs/OBSERVATION_CONTRACT.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OPTIONAL_YOLO.md`
- `docs/EXPORTS.md`
- `docs/PROVENANCE_AUDIT.md`
- `docs/COMPLETION_CHECKLIST.md`
- `docs/CONTROL_ROOM_INDEX.md`

## Boundary Checklist

Confirm TOM v3 Simple still does not add:

- real pose inference
- movement interpretation
- stroke classification
- serve or hit conclusions
- bounce detection
- rally segmentation
- point reconstruction
- scoring
- homography
- adjudication

## Validation Checklist

Run:

```bash
pytest -q
ruff check .
```

Run web validation:

```bash
cd apps/web
npm run lint
npm run build
npm audit --omit=dev
```

Run migration smoke:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
```

Run synthetic viewer smoke:

```bash
python scripts/smoke_synthetic_viewer_data.py
```

Optional YOLO check:

```bash
make yolo-probe
make yolo-smoke
```

## Final Completion Checklist

- `make demo` passes.
- `make completion-audit` passes.
- Viewer shows detections, tracklets, pose evidence, lineage, artifacts, annotations, and exports.
- Exports are created.
- Known limitations are documented.
- Optional YOLO is documented and separate from the default fixture demo.
- Observation-only boundary is clear.
- No out-of-scope capabilities were added.
