# Milestone 7E - Court / Homography Evidence Decision Gate

## Status

Complete.

## Goal

Decide whether court/camera/homography evidence belongs inside Blueprint 7 or should become a separate blueprint.

## Decision

Court / camera / homography evidence should be deferred to Blueprint 8.

Blueprint 7 should remain focused on real detection replay, real-detection-derived candidate tracklets, real pose keypoint evidence, and final orchestration/closeout.

## What Changed

- Added a court/homography evidence decision note.
- Added a Blueprint 8 candidate document for court/camera/homography evidence.
- Proposed future court observation family and observation types.
- Proposed future court keypoint, court line, camera/view, and homography candidate contracts.
- Proposed future lineage, replay overlay, review label, and export contracts.
- Updated canonical status docs to make the Blueprint 8 deferral explicit.

## Boundary

7E adds no court runtime, database migration, API endpoint, frontend court overlay, homography computation, coordinate transform service, event logic, stream ingestion, or adjudication.

Court/homography belongs in Blueprint 8.
