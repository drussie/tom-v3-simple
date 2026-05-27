# Milestone 8D Handoff - Homography Candidate Persistence

Repo: `drussie/tom-v3-simple`

Branch: `codex/m8d-homography-candidate-persistence`

Starting point: Milestone 8C Camera / View Evidence Layer accepted and merged to `main`.

## Mission

Persist homography candidate observations from persisted court keypoint, court line, and camera/view evidence while preserving TOM v3's observation-only geometry boundary.

## Implemented Flow

```text
indexed media
-> run-fixture-court
-> build-homography-candidates
-> homography_candidate_observation rows
-> lineage from court keypoints, court lines, and camera/view context
```

## Commands

```bash
.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id <media_id> \
  --court-run-id <court_run_id>
```

```bash
make homography-candidates \
  MEDIA_ID=<media_id> \
  COURT_RUN_ID=<court_run_id> \
  PYTHON=.venv/bin/python
```

Plan-only:

```bash
.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id media-plan \
  --court-run-id court-run-plan \
  --plan-only
```

## Preserved Boundaries

8D does not add projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## Recommended Next Handoff

Milestone 8E - Court Overlay in Replay Workstation.
