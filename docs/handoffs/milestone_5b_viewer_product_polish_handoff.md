# TOM v3 Simple - Milestone 5B Handoff

## Viewer / Product Polish

Repo: drussie/tom-v3-simple

Branch: `codex/m5b-viewer-product-polish`

Starting state: Milestone 5A Local Demo / Runbook Completion Path accepted and merged to main.

## Status

Milestone 5B is complete.

Blueprint 5 remains a completion and product-hardening pass.

## Completed Path

```text
viewer run payload
-> run evidence summary
-> clearer empty states
-> detection observation detail
-> tracklet candidate evidence
-> pose keypoint evidence
-> readable lineage/source context
-> artifact and annotation detail
-> review export summary when available
```

## Main Entry Points

Run the canonical fixture demo:

```bash
make demo
```

Open a viewer URL from the demo summary:

```text
http://127.0.0.1:3000/runs/<run_id>
```

Read the viewer polish doc:

```text
docs/web/viewer_product_polish_v0.md
```

## Notes For The Next Agent

- The product surface now uses more consistent observation/evidence/candidate wording.
- Empty states point to practical next local commands instead of leaving panels blank.
- The viewer has a run evidence summary panel for run context, counts, annotations, lineage, and review exports.
- Tracklet rows use candidate wording.
- Pose rows use keypoint evidence wording.
- Annotation rows expose keypoint metadata and review-only context.
- This milestone did not add new runtime capability or tennis interpretation.

## Next Recommended Handoff

Milestone 5C - Final Evidence / Provenance Audit

Keep Blueprint 5 focused on completion and product hardening. Do not add new tennis interpretation capability.
