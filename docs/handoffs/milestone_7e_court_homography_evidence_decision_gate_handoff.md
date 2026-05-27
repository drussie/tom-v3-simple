# TOM v3 - Milestone 7E Handoff

## Court / Homography Evidence Decision Gate

Repo: `drussie/tom-v3-simple`

Branch: `codex/m7e-court-homography-evidence-decision-gate`

Starting state: Milestone 7D Real Pose Runtime for Replay Workstation completed and merged to `main`.

## Mission

Document the decision that court/camera/homography evidence should be deferred to Blueprint 8.

The 7E path is:

```text
Blueprint 7 real perception runtime
-> court/homography scope review
-> decision gate
-> Blueprint 8 candidate
-> no runtime implementation
```

## Required Boundary

Use evidence language:

- court evidence
- court keypoint observation
- court line evidence
- camera/view evidence
- homography candidate
- projection evidence
- coordinate transform candidate
- geometry evidence
- future Blueprint 8

Do not add court runtime, homography computation, court overlays, court-space coordinate transforms, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Validation Checklist

- Court/homography decision doc exists.
- Blueprint 8 candidate doc exists.
- Proposed court evidence contracts are documented.
- Proposed lineage, replay, review, and export ideas are documented.
- Canonical status docs state that court/homography is deferred to Blueprint 8.
- Existing tests/builds pass.
- No code runtime or schema migration is added.

## Recommended Next Handoff

Milestone 7F - Perception Run Orchestration and Completion Review.
