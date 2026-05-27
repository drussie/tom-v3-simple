# TOM v3 Simple - Milestone 5A Handoff

## Local Demo / Runbook Completion Path

Repo: drussie/tom-v3-simple

Branch: `codex/m5a-local-demo-runbook-completion-path`

Starting state: Blueprints 1, 2, 3, and 4 complete.

## Status

Milestone 5A is complete.

Blueprint 5 has started as a completion and product-hardening pass.

## Completed Path

```text
index media
-> fixture gameplay observations
-> fixture detections
-> frame-backed artifacts
-> candidate tracklets
-> fixture pose observations
-> review annotations
-> pose and tracklet review exports
-> viewer URLs
```

## Main Entry Points

Run the canonical fixture demo:

```bash
make demo
```

Preview the plan:

```bash
make demo-plan
```

Run directly:

```bash
python -m apps.worker.cli run-demo
```

Read the canonical local runbook:

```text
docs/RUNBOOK_LOCAL.md
```

## Notes For The Next Agent

- The default demo does not require YOLO weights or real pose weights.
- If no custom media is supplied, the demo can generate a tiny synthetic placeholder media file and marks it as synthetic demo media.
- `demo-reset` is intentionally non-destructive.
- Optional YOLO smoke remains separate through `make yolo-probe` and `make yolo-smoke`.
- Fixture output is evidence plumbing only.

## Next Recommended Handoff

Milestone 5B - Viewer / Product Polish

Keep Blueprint 5 focused on completion and product hardening. Do not add new tennis interpretation capability.
