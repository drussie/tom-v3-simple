# Milestone 0C Handoff - Worker + Rich Synthetic Observation Seeder

## Repo

- Repo: drussie/tom-v3-simple
- Branch: codex/m0c-worker-synthetic-pipeline

## Mission

Implement the first worker layer and rich synthetic observation seeding flow for TOM v3 Simple.

TOM v3 Simple is:

> A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Boundary

TOM v3 is observation-only.

Core invariant:

> TOM v3 records what was observed, not what was proven.

Milestone 0C does not add real ML, real video processing, real tracking, real bounce logic, or a frontend viewer.

## Result

Status: complete.

Milestone 0C created:

- Worker package and CLI in `apps/worker`.
- Shared rich synthetic seeder in `packages/observations/tom_v3_observations/synthetic.py`.
- Baseline scenario wrapper in `apps/worker/scenarios/baseline_tennis_clip.py`.
- API dev route reuse of the shared seeding function.
- Tests for worker/seeder behavior.
- Worker docs and updated project memory.

## CLI

Seed a baseline run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db \
python -m apps.worker.cli seed-synthetic-run \
  --scenario baseline-tennis-clip \
  --source-uri file:///dev/synthetic-tennis-clip.mp4 \
  --run-name synthetic-baseline-run
```

Verify a seeded run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db \
python -m apps.worker.cli verify-synthetic-run --run-id <run_id>
```

## Seeded Evidence

The baseline scenario creates:

- 4 view-state observations: gameplay, non_gameplay, uncertain, gameplay.
- 7 ball observations.
- 8 player observations across near-player and far-player tracks.
- 3 tracklets.
- 15 track points.
- 3 homography placeholder observations, including one missing interval.
- 1 bounce_candidate.
- 1 tracking_gap_candidate.
- 1 hit_candidate.
- lineage from candidates to supporting observations.
- 6 placeholder evidence artifacts.

## Known Gaps

- No actual media file is required or inspected.
- No artifact files are generated; artifact records point to placeholder `file:///dev` URIs.
- Homography records are generic atomic observations because typed homography tables are not implemented yet.
- The worker uses SQLAlchemy models directly and the shared observation writer.

## Recommended Next Handoff

Milestone 0D - Visual Evidence Viewer Foundation.

Suggested focus:

- Build the first web viewer against the seeded baseline data.
- Show timeline bands for view state, track coverage, homography availability, and candidates.
- Use API/query/detail/lineage/artifact endpoints rather than frontend-only fixture data.
- Keep real ML integration out of scope.
