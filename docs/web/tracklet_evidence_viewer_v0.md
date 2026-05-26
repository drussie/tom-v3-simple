# Tracklet Evidence Viewer v0

## Purpose

Tracklet Evidence Viewer v0 adds a focused multi-run inspection panel to the existing run viewer.

The viewer remains opened on one run:

```text
/runs/{tracklet_run_id}
```

When a user selects a tracklet candidate, the web app calls:

```text
GET /tracklets/{tracklet_id}/evidence-bundle
```

## Viewer Behavior

The panel shows:

- tracklet candidate id and observation id
- track family and subject reference
- candidate / unverified status
- frame range and confidence
- source detection run id
- track point candidates
- selected source detection observation
- matched frame artifact image when available
- bbox metadata when no frame artifact is available
- lineage row ids for `tracked_from` and `grouped_from`
- review annotation summaries
- review controls for selected tracklet, track point, or source detection observations

## Multi-Run Scope

This is not a full multi-run timeline. The viewer stays lightweight:

1. open the tracklet builder run
2. choose a tracklet candidate
3. load evidence from the source detection run inside the panel
4. drill from tracklet to track point to source detection

## Language Contract

Use:

- tracklet candidate
- track point candidate
- source detection
- visual evidence
- lineage

Avoid language that implies a confirmed trajectory, identity, event, rally, point state, or score.

## Known Limitations

- The source detection overlay and tracklet coverage are not yet fused into one multi-run timeline.
- Review annotations use a local/dev reviewer value until auth exists.
- Frame images appear only when frame artifacts have already been extracted.
