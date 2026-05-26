# Milestone 0D Handoff - Visual Evidence Viewer Foundation

## Repo

- Repo: drussie/tom-v3-simple
- Branch: codex/m0d-visual-evidence-viewer

## Mission

Build the first visual evidence viewer for TOM v3 Simple.

TOM v3 Simple is:

> A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation - including gameplay/non-gameplay state - and makes the evidence queryable and visually replayable without adjudicating truth.

## Boundary

TOM v3 is observation-only.

Core invariant:

> TOM v3 records what was observed, not what was proven.

Milestone 0D does not add real ML, real video processing, real tracking, real homography calculation, real bounce logic, production auth, or deployment.

## Result

Status: complete.

Milestone 0D created:

- Next.js web app in `apps/web`.
- Run viewer route at `/runs/{run_id}`.
- Data-driven timeline rows for view state, track coverage, homography, and candidates.
- Observation list and detail panel.
- Lineage, artifact, and annotation panels.
- Thin backend viewer endpoint `GET /viewer/runs/{run_id}`.
- Tests for viewer endpoint composition.
- Web docs and updated project memory.

## Viewer Data Contract

The viewer uses:

- `GET /viewer/runs/{run_id}` for composed viewer data.
- Existing persisted observations for the observation spine.
- Tracklet metadata for coverage rows and missingness.
- Derived observation rows for candidate markers.
- Lineage rows for supporting observation relationships.
- Evidence artifact metadata for placeholder artifacts.
- Human annotation rows for annotation display.

The endpoint is a read model over stored evidence. It does not create observations or add new interpretation logic.

## Local Demo

Seed a synthetic run, start the API, then start the web app:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db \
.venv/bin/python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip
```

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db \
TOM_V3_CREATE_DB_ON_STARTUP=true \
.venv/bin/uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open `/runs/<run_id>`.

## Known Gaps

- No real media playback yet.
- Annotation creation remains a panel foundation in the web app.
- Viewer-specific API is intentionally a read composition endpoint.
- No E2E test harness is configured yet.
- Placeholder artifact URIs remain metadata only.

## Recommended Next Handoff

Milestone 0E - Integration / QA / Repo Consolidation.
