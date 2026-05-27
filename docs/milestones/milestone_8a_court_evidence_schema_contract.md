# Milestone 8A - Court Evidence Schema / Contract

## Status

Complete.

## Goal

Start Blueprint 8 by implementing the court/camera/homography evidence schema contract and typed persistence foundation.

## What 8A Adds

- `tom_v3_schema.court` with court keypoint, line, camera/view, homography candidate, projection diagnostic, and court template contracts.
- `tennis_court_template_normalized_v0` registry entry.
- Typed storage models for five court evidence observation tables.
- Alembic migration `0003_court_evidence_observations`.
- Observation writer support for typed court evidence rows.
- Lineage relationship constants for homography and projection diagnostic provenance.
- Schema and persistence tests using fake court evidence.
- Court schema/template docs and canonical status updates.

## What 8A Does Not Add

- real court keypoint detector
- real court line detector
- homography computation runtime
- replay court overlay
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- real stream ingestion
- adjudication

## Boundary

Court evidence remains candidate geometry evidence. It is persisted, queryable at the storage layer, and lineage-ready, but it does not produce tennis-event or court-position conclusions.
