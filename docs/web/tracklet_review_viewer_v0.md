# Tracklet Review Viewer v0

## Purpose

Tracklet Review Viewer v0 extends the Tracklet Evidence panel with basic review controls.

## Behavior

When a tracklet builder run is opened at:

```text
/runs/{tracklet_run_id}
```

the viewer can:

- select a tracklet candidate
- load the tracklet evidence bundle
- show annotation summaries for the selected tracklet, track point, and source detection
- add a review annotation to the selected tracklet candidate observation
- add a review annotation to the selected track point candidate observation
- add a review annotation to the selected source detection observation
- refresh the evidence bundle after the annotation is saved

## Local Reviewer

Milestone 2C does not add authentication. The viewer writes review annotations with the local/dev reviewer value:

```text
local-reviewer
```

## Language Contract

The UI uses candidate/review/evidence language. A review annotation is not a correction, promotion, or adjudication. It is another persisted observation about the reviewer's assessment.

## Known Limitations

- There is no production review queue.
- Annotation labels are documented and offered in the viewer, but no enum migration is added.
- The review viewer itself does not save query results. Milestone 2D export can save `query_result` rows for query-based review dataset exports.

## Blueprint 2 Completion

Milestone 2E confirms viewer review controls as the Blueprint 2 review surface. Review annotations are non-mutating evidence and remain separate from candidate tracklet, track point, and source detection observations.
