# TOM v3 - Milestone 8A Handoff

## Court Evidence Schema / Contract

Repo: `drussie/tom-v3-simple`

Branch: `codex/m8a-court-evidence-schema-contract`

Starting state: TOM v3 Simple, Blueprint 6, and Blueprint 7 are complete.

## Mission

Start Blueprint 8 with schema and persistence contracts for court/camera/homography evidence.

The implemented path is:

```text
observation spine
-> typed court keypoint / line / camera / homography / projection diagnostic rows
-> lineage between source court evidence and geometry candidates
-> docs and tests
```

## Required Boundary

8A is schema/contract only.

Do not add court runtime, replay court overlay, homography computation, ball/player court projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## Recommended Next Step

Milestone 8B - Court Keypoint / Line Evidence Adapter.
