# TOM v3 Simple Provenance Audit

Milestone 5C adds a structural evidence/provenance audit for the local TOM v3 Simple demo path.

The audit checks whether persisted demo evidence is internally coherent. It does not check model correctness and does not decide tennis meaning.

## What It Checks

The audit covers:

- demo media ownership and media metadata
- processing run and processing step references
- observation media/run/frame/time ownership
- typed-row integrity for atomic, gameplay, pose, tracklet, and track point evidence
- candidate tracklet and track point references
- pose keypoint structure and media-owned frame/time
- lineage parent and child observation references
- artifact media/run/target references
- annotation media/observation/artifact references
- pose and tracklet review export artifacts
- demo completeness for media, runs, observations, lineage, artifacts, annotations, and exports

The audit is intentionally structural. It does not evaluate whether a bbox, tracklet candidate, pose keypoint, or annotation is correct.

## Result Semantics

The CLI returns JSON with:

- `status = passed`: all required checks passed and no warning checks failed.
- `status = warning`: required checks passed, but warning-severity checks found gaps.
- `status = failed`: a fail-severity check found a structural problem.
- `ok = false`: the command should be treated as failed.

`--strict` treats warning-severity findings as command failures.

The output also includes:

- `summary`: media/run/step/observation/lineage/artifact/annotation/export counts.
- `checks`: every check with status, severity, message, count, and details.
- `warnings`: warning checks that found issues.
- `failures`: failed checks.
- `observation_only = true`
- `no_adjudication = true`

## Run The Audit

Run the fixture demo first:

```bash
make demo
```

Then run:

```bash
make completion-audit
```

Equivalent worker command:

```bash
python -m apps.worker.cli completion-audit --demo-only
```

Audit all local rows instead of only demo-marked media:

```bash
python -m apps.worker.cli completion-audit --no-demo-only
```

Audit one media row:

```bash
python -m apps.worker.cli completion-audit --media-id <media_id>
```

Treat warnings as failures:

```bash
python -m apps.worker.cli completion-audit --demo-only --strict
```

## Makefile Targets

`make completion-audit` runs the demo-scoped audit.

`make completion-check` still runs the lightweight validation path and prints how to run the full provenance audit. To require the audit inside `completion-check`, run:

```bash
TOM_V3_AUDIT_REQUIRED=true make completion-check
```

This keeps empty local databases from failing the default checklist before a demo has been created.

## Expected Demo Path

In demo-only mode, the audit expects:

- one demo media asset marked with `tom_v3_demo = true`
- fixture gameplay, detection, tracklet, and pose runs
- ball/player detection observations
- candidate tracklets and track points
- pose observations
- evidence artifacts, including frame images
- seeded review annotations
- pose review export artifact
- tracklet review export artifact
- lineage between detections, track points, tracklets, and source-associated pose observations

If no demo media exists, `completion-audit --demo-only` fails with:

```text
No demo media found. Run make demo first.
```

## Non-Goals

The provenance audit does not add or evaluate:

- real pose inference
- movement interpretation
- stroke classification
- serve, hit, split-step, or biomechanics conclusions
- homography
- bounce detection
- hit detection
- rally or point reconstruction
- scoring
- adjudication
- model correctness
