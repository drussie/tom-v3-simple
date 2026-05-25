# Milestone 0A Handoff - Repo Memory + Architecture / Schema Foundation

## Repo

- Repo: drussie/tom-v3-simple
- Branch: codex/m0a-repo-memory-architecture-schema

## Mission

Create the first durable foundation for TOM v3 Simple.

TOM v3 Simple is:

> A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Boundary

TOM v3 is observation-only.

Use vocabulary such as:

- observation
- atomic_observation
- derived_observation
- candidate
- signal
- track
- tracklet
- track_point
- gameplay_observation
- view_state_observation
- evidence_artifact
- human_annotation
- query_result
- lineage

Core invariant:

> TOM v3 records what was observed, not what was proven.

## Milestone 0A Scope

Create the repo-backed memory and architecture foundation.

This milestone does not implement real model processing, YOLO integration, TOM v1 integration, bounce detection, or the full frontend.

## Created Structure

```text
docs/
  CONTROL_ROOM_INDEX.md
  CURRENT_STATE.md
  BLUEPRINT_PROGRESS.md
  IMPLEMENTATION_LOG.md
  architecture/
    tom_v3_observation_platform_blueprint_v0_1.md
    observation_store_v0.md
    visual_evidence_viewer_v0.md
    gameplay_view_state_layer_v0.md
    github_as_memory_workflow_v0.md
  milestones/
    milestone_0_observation_store_visual_foundation.md
    milestone_0a_repo_memory_architecture_schema.md
  handoffs/
    milestone_0a_repo_memory_architecture_schema_handoff.md
  agent_reports/
    milestone_0a_repo_memory_architecture_schema_report.md
```

## Acceptance Status

Status: complete.

Milestone 0A acceptance criteria are satisfied by the documentation spine, architecture docs, schema contract, handoff doc, agent report, updated README, and placeholder tracked skeleton directories.

## Recommended Next Handoff

Milestone 0B - Backend / API Foundation.

Suggested focus:

- Choose initial backend stack.
- Create first database migrations from `docs/architecture/observation_store_v0.md`.
- Add API contracts for media, runs, observations, evidence artifacts, lineage, and annotations.
- Preserve append-only observation behavior.
- Keep real ML integration out of scope.
