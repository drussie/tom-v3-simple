# Visual Evidence Viewer v0

## Purpose

Visual Evidence Viewer v0 is the first TOM v3 Simple web surface for inspecting persisted observations.

The core UI contract is:

```text
The database says this observation exists. Show me the evidence.
```

The viewer is data-driven from backend rows. It does not maintain a separate frontend-only evidence model.

## App Location

```text
apps/web
```

Key files:

- `src/app/page.tsx`
- `src/app/runs/[runId]/page.tsx`
- `src/components/EvidenceViewer.tsx`
- `src/components/Timeline.tsx`
- `src/components/TrackCoverageRows.tsx`
- `src/components/CandidateMarkers.tsx`
- `src/components/ObservationList.tsx`
- `src/components/ObservationDetailPanel.tsx`
- `src/components/LineagePanel.tsx`
- `src/components/ArtifactPanel.tsx`
- `src/components/AnnotationPanel.tsx`
- `src/lib/api.ts`
- `src/lib/viewerData.ts`
- `src/lib/timeline.ts`
- `src/lib/types.ts`

## API Routes Used

Primary route:

- `GET /viewer/runs/{run_id}`

The viewer read model contains:

- run metadata
- media metadata
- processing steps
- observations with typed detail
- tracklets and track points
- lineage rows
- artifact metadata
- annotation rows

The endpoint composes existing backend storage rows. It does not write observations.

## Viewer Rows

The first viewer renders:

- Gameplay: `gameplay`, `non_gameplay`, and `uncertain`
- Ball track: tracked, gap, tracked, low_confidence
- Near player: tracked, gap, tracked
- Far player: gap, tracked, tracked
- Homography: valid, missing, valid
- Candidates: `bounce_candidate`, `tracking_gap_candidate`, and `hit_candidate`

Rows are built from observation rows and tracklet metadata created by the synthetic baseline scenario.

## Detail Panels

Selecting a segment, candidate marker, or observation row updates:

- observation detail
- typed detail
- payload JSON
- lineage rows
- artifact metadata
- annotation display

Annotation creation is not wired in v0. The panel is present so the viewer layout reserves the workflow without mutating observations.

## Local Development

Install web dependencies:

```bash
cd apps/web
npm install
```

Seed a synthetic run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db \
.venv/bin/python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip
```

Start backend:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db \
TOM_V3_CREATE_DB_ON_STARTUP=true \
.venv/bin/uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

Start frontend:

```bash
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/runs/<run_id>
```

## Known Limitations

- No real video file is required or played.
- Placeholder artifact URIs are displayed as metadata.
- The annotation panel is read-only in v0.
- The viewer focuses on baseline synthetic evidence shape.
- Production deployment, auth, and streaming are out of scope.
