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
- `src/components/DetectionOverlayPanel.tsx`
- `src/components/DetectionOverlayCanvas.tsx`
- `src/components/LineagePanel.tsx`
- `src/components/ArtifactPanel.tsx`
- `src/components/AnnotationPanel.tsx`
- `src/lib/api.ts`
- `src/lib/detections.ts`
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
- Detections: `ball_detection` and `player_detection` markers when persisted bboxes exist

Rows are built from observation rows and tracklet metadata created by the synthetic baseline scenario.

Milestone 2A lets the viewer open tracklet-builder runs with first-class track observations. These runs include `ball_tracklet_candidate` / `player_tracklet_candidate` observations, `track_point_candidate` observations, candidate `tracklet` and `track_point` rows, and lineage from source detections to track points and from track points to tracklets.

Milestone 2B adds a Tracklet Evidence panel. Selecting a tracklet candidate calls `GET /tracklets/{tracklet_id}/evidence-bundle` and displays source detection observations, matched frame artifacts, and lineage from the source detection run without turning the whole page into a full multi-run timeline.

## Detection Overlay

Milestone 1D adds a detection overlay panel. It extracts persisted `ball_detection` and `player_detection` observations from the viewer run payload, reads bbox payloads from the observation spine or atomic extension, and scales them using persisted media dimensions.

Milestone 1E adds frame artifact support. If a matching extracted frame artifact exists, the panel displays the frame image behind the persisted bboxes. If no real frame image is available, the panel renders an `image_pixels` coordinate canvas. This keeps the viewer honest while still answering where the detection was observed.

Selecting a detection observation shows all bboxes on the same frame and highlights the selected bbox. Selecting a bbox updates the existing observation detail, lineage, artifact, and annotation panels.

## Detail Panels

Selecting a segment, candidate marker, or observation row updates:

- observation detail
- typed detail
- payload JSON
- lineage rows
- artifact metadata
- annotation display

The general side annotation panel remains simple. Milestone 2C wires review annotation creation in the Tracklet Evidence panel for selected tracklet candidate, track point candidate, and source detection observations.

## Tracklet Review

When a tracklet builder run is open, selecting a tracklet loads `GET /tracklets/{tracklet_id}/evidence-bundle`. The Tracklet Evidence panel can show annotation summaries and create review annotations through the existing `human_annotation` API. The viewer remains a single-run page while the focused panel displays source detection evidence from the source run.

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
- The general annotation panel is read-only; tracklet review annotations are created in the focused Tracklet Evidence panel.
- Detection overlays use a coordinate canvas when no frame image artifact is available.
- Local artifact content serving is development-only.
- The viewer is still a single-run view; cross-run evidence appears only in the focused Tracklet Evidence panel.
- Production deployment, auth, and streaming are out of scope.
