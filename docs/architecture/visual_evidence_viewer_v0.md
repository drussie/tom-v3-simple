# Visual Evidence Viewer v0

## Purpose

TOM v3 must be visual from the beginning.

The viewer is the operational way to inspect observations, missingness, lineage, confidence, artifacts, and human annotations.

## Key UI Contract

> The database says this observation exists. Show me the evidence.

The UI must make it obvious:

- what was tracked
- what was not tracked
- where tracking started
- where tracking ended
- where tracking dropped
- where gameplay was detected
- where non-gameplay was detected
- where observations/candidates exist
- what evidence supports each observation

Missingness is evidence. Do not hide missing tracking.

## Future Viewer Surface

The viewer should eventually show:

- video player
- overlay canvas
- gameplay/non-gameplay/uncertain timeline band
- track coverage rows
- ball track
- near-player track
- far-player track
- pose availability
- homography validity
- candidate markers
- tracking gaps
- low-confidence regions
- observation detail panel
- lineage panel
- artifact panel
- annotation panel

## Viewer Data Contract

The viewer should be fed by queryable observations and artifacts rather than bespoke transient processing output.

Expected viewer data should include:

- media metadata
- frame/time index
- processing runs and steps
- observation ranges
- tracklets and track points
- derived observations and candidates
- evidence artifacts
- lineage relationships
- human annotations

## Review Behavior

The viewer should support inspection and annotation. It should not mutate previous observations when a user disagrees with a model output.

Human review creates human_annotation records linked to observations, artifacts, frames, or time ranges.

## Milestone 0D Direction

Milestone 0D should build a first viewer against synthetic observations. The first version does not need full product polish, but it must prove the loop:

```text
query observations -> show timeline/overlays -> inspect details -> inspect lineage/artifacts
```
