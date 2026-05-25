# Synthetic Seeder v0

## Purpose

Synthetic Seeder v0 creates rich persisted TOM v3 observations without real ML or real video processing.

It exists to feed the future visual evidence viewer with realistic observation shapes:

```text
worker command
  -> register media metadata
  -> create processing run
  -> create processing steps
  -> seed observations, tracklets, gaps, candidates, lineage, artifacts
  -> verify queryable evidence
```

## Commands

Seed:

```bash
python -m apps.worker.cli seed-synthetic-run \
  --scenario baseline-tennis-clip \
  --source-uri file:///dev/synthetic-tennis-clip.mp4 \
  --run-name synthetic-baseline-run
```

Verify:

```bash
python -m apps.worker.cli verify-synthetic-run --run-id <run_id>
```

Use `TOM_V3_DATABASE_URL` to choose the database. The CLI creates tables by default for local development; pass `--skip-create-db` when migrations already manage the schema.

## Shared Code Path

Both the worker CLI and `POST /dev/synthetic-run` call the shared seeding library in:

```text
packages/observations/tom_v3_observations/synthetic.py
```

This prevents API-owned synthetic logic from diverging from the worker path.

## Rerun Behavior

Default behavior creates a new processing run each time.

Observation idempotency keys include the run id. This keeps each seeded run internally retry-safe without collapsing separate development runs into one set of observations.

## Output

The seed command prints JSON containing:

- media id
- runtime config id
- model id
- processing run id
- processing step ids
- observation ids grouped by type
- tracklet ids
- track point count
- artifact count
- lineage count
- verification result

## Still Synthetic

The seeder does not decode media, run detectors, calculate homography, track players, or infer tennis outcomes. It records synthetic observations shaped like future model output.
