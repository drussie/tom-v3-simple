# TOM v3 Simple - Control Room Index

TOM v3 is an observation-only platform.
It records evidence.
It does not adjudicate truth.

Use this index as the durable navigation point for project memory, architecture decisions, milestone state, handoffs, and agent reports.

## Current Project State

- [Current State](CURRENT_STATE.md)
- [Blueprint Progress](BLUEPRINT_PROGRESS.md)
- [Implementation Log](IMPLEMENTATION_LOG.md)

## Architecture

- [TOM v3 Observation Platform Blueprint v0.1](architecture/tom_v3_observation_platform_blueprint_v0_1.md)
- [Observation Store v0](architecture/observation_store_v0.md)
- [Gameplay / View-State Layer v0](architecture/gameplay_view_state_layer_v0.md)
- [Visual Evidence Viewer v0](architecture/visual_evidence_viewer_v0.md)
- [GitHub-as-Memory Workflow v0](architecture/github_as_memory_workflow_v0.md)

## Milestones

- [Milestone 0 - Observation Store + Visual Foundation](milestones/milestone_0_observation_store_visual_foundation.md)
- [Milestone 0A - Repo Memory + Architecture / Schema Foundation](milestones/milestone_0a_repo_memory_architecture_schema.md)
- [Milestone 0B - Backend / API Foundation](milestones/milestone_0b_backend_api_foundation.md)
- [Milestone 0C - Worker + Synthetic Observation Seeder](milestones/milestone_0c_worker_synthetic_observation_seeder.md)
- [Milestone 0D - Visual Evidence Viewer Foundation](milestones/milestone_0d_visual_evidence_viewer_foundation.md)
- [Milestone 0E - Integration / QA / Repo Consolidation](milestones/milestone_0e_integration_qa_repo_consolidation.md)

## Handoffs

- [Milestone 0A Handoff](handoffs/milestone_0a_repo_memory_architecture_schema_handoff.md)
- [Milestone 0B Handoff](handoffs/milestone_0b_backend_api_foundation_handoff.md)
- [Milestone 0C Handoff](handoffs/milestone_0c_worker_synthetic_observation_seeder_handoff.md)
- [Milestone 0D Handoff](handoffs/milestone_0d_visual_evidence_viewer_foundation_handoff.md)
- [Milestone 0E Handoff](handoffs/milestone_0e_integration_qa_repo_consolidation_handoff.md)

## Agent Reports

- [Milestone 0A Agent Report](agent_reports/milestone_0a_repo_memory_architecture_schema_report.md)
- [Milestone 0B Agent Report](agent_reports/milestone_0b_backend_api_foundation_report.md)
- [Milestone 0C Agent Report](agent_reports/milestone_0c_worker_synthetic_observation_seeder_report.md)
- [Milestone 0D Agent Report](agent_reports/milestone_0d_visual_evidence_viewer_foundation_report.md)
- [Milestone 0E Agent Report](agent_reports/milestone_0e_integration_qa_repo_consolidation_report.md)

## API and Schema

- [Backend API v0](api/backend_api_v0.md)
- [Database Schema v0](schema/database_schema_v0.md)

## Worker

- [Synthetic Seeder v0](worker/synthetic_seeder_v0.md)
- [Baseline Synthetic Scenario v0](worker/synthetic_scenario_baseline_v0.md)

## Web

- [Visual Evidence Viewer v0](web/visual_evidence_viewer_v0.md)

## Development

- [Local Environment Setup](dev/local_environment_setup.md)
- [Local Demo Runbook](dev/local_demo_runbook.md)
- [Repo Branch Hygiene](dev/repo_branch_hygiene.md)

## Core Vocabulary

Preferred TOM v3 vocabulary:

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
