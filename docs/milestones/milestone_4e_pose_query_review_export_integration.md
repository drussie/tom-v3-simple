# Milestone 4E - Pose Query / Review / Export Integration

## Status

Status: complete.

## Goal

Make persisted pose evidence searchable, annotatable through the generic review annotation path, and exportable as a TOM-native review dataset without adding pose inference or movement interpretation.

## What Changed

- Added pose-specific query filters for run/media/frame/time, confidence, missing keypoint count, skeleton format, and subject association fields.
- Added pose evidence bundle assembly with pose detail, source candidate context, lineage, artifacts, annotations, model, and runtime config summaries.
- Added pose review label vocabulary and keypoint-level annotation metadata support through the existing `human_annotation` table.
- Added TOM-native pose review dataset export with local JSON artifacts, `evidence_artifact` metadata, checksum, and query result memory.
- Added API endpoints for pose query, pose evidence bundle, and pose review export.
- Added worker CLI `export-pose-review-dataset`.

## Evidence Boundary

A pose observation remains keypoint evidence produced for a media-owned frame/time. Review annotations are additional evidence records; they do not mutate pose observations or source observations.

The export packages pose observations, keypoints, source association candidate context, lineage, artifacts, and annotations. It does not create movement conclusions, event conclusions, scoring, or adjudication.

## Validation

Focused tests cover pose query filters, pose evidence bundles, pose annotations, keypoint-level metadata, and pose review export artifacts.

## Next

Recommended next milestone: Milestone 4F - Blueprint 4 Completion Review / Pose Evidence Hardening.
