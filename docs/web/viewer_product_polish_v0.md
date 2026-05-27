# Viewer Product Polish v0

## Purpose

Viewer Product Polish v0 makes the existing TOM v3 Simple Evidence Viewer easier to understand during the local fixture demo.

It does not introduce a new viewer, new model runtime, or new tennis interpretation layer. It improves labels, empty states, source-context display, annotation display, and export visibility around already persisted evidence.

## Primary Files

- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/components/RunEvidenceSummary.tsx`
- `apps/web/src/components/ObservationList.tsx`
- `apps/web/src/components/ObservationDetailPanel.tsx`
- `apps/web/src/components/DetectionOverlayPanel.tsx`
- `apps/web/src/components/TrackletEvidencePanel.tsx`
- `apps/web/src/components/PoseOverlayPanel.tsx`
- `apps/web/src/components/LineagePanel.tsx`
- `apps/web/src/components/ArtifactPanel.tsx`
- `apps/web/src/components/AnnotationPanel.tsx`
- `apps/web/src/lib/evidenceCopy.ts`

## Run Evidence Summary

The viewer now includes a run-level summary panel with:

- processing run id, status, adapter, and timestamps
- model and runtime config ids when present
- observation counts by evidence type
- lineage row count
- annotation count
- visible review export artifacts, URI, checksum, and record count metadata when the viewer payload includes them

The summary explicitly frames the page as persisted observation evidence and review context.

## Empty States

Empty states are now more explicit for:

- no media metadata
- no observations in a run
- no detection observations or frame artifacts
- no loaded tracklet evidence bundle
- no pose observations
- no lineage rows
- no artifacts
- no review annotations
- no review export artifacts visible in the current run payload

The empty-state copy points to local commands where useful, such as `make demo`, `run-detection-adapter`, `extract-frame-artifacts`, `build-tracklets`, `run-pose-adapter`, and review export commands.

## Terminology

User-visible labels prefer:

- detection observation
- ball detection observation
- player detection observation
- tracklet candidate
- track point candidate
- pose observation
- keypoint evidence
- source detection observation
- subject association candidate
- evidence artifact
- review annotation
- lineage

The viewer avoids implying that fixture outputs or model outputs are correct tennis understanding.

## Detection Panel

The detection panel now clarifies that detection observations are model or fixture outputs. It shows the bbox overlay path when evidence exists and gives a concrete next step when frame artifacts are missing.

Detection overlay logic is unchanged: persisted image-pixel bbox payloads are scaled into the displayed media coordinate space.

## Tracklet Panel

The tracklet panel now presents candidate temporal grouping language and gives an empty state when no tracklet evidence bundle is loaded.

Relationship descriptions are human-readable:

- `tracked_from` means a source detection was grouped into a track point candidate.
- `grouped_from` means a track point candidate was grouped into a tracklet candidate.
- `pose_from_subject_detection_candidate` means a pose observation was generated from source player detection candidate context.
- `subject_context_candidate` means a pose observation has candidate subject context from a tracklet.
- `pose_from_track_point_candidate` means a pose observation has candidate subject context from a track point.

Raw relationship types remain visible as technical detail.

## Pose Panel

The pose panel now emphasizes keypoint evidence. It explains that pose observations do not classify movement, actions, or biomechanics.

Missing keypoints remain visible in the table and are not rendered as present markers. Existing COCO17 skeleton rendering behavior is unchanged.

## Annotation Panel

The annotation panel now states that annotations are non-mutating review evidence.

Rows display:

- annotation label/type
- creator
- frame range
- notes when present
- keypoint name/index when present
- demo-seeded and review-only metadata flags when present

Annotations do not mutate observations, source detections, tracklet candidates, pose observations, or exports.

## Artifact And Export Display

Artifact rows now show target observation context, URI, checksum, created timestamp, and review export record counts when metadata is present.

The run summary shows review dataset export artifacts when the viewer payload includes them. If export artifacts are not present for a selected run, the viewer gives the relevant export commands rather than creating a new export surface.

## Non-Goals

- No new backend model capability.
- No real pose inference.
- No movement interpretation.
- No stroke classification.
- No homography.
- No bounce, hit, rally, point, or scoring logic.
- No adjudication.
- No major frontend redesign.
