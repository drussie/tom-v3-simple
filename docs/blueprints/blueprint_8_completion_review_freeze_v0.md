# Blueprint 8 Completion Review / Freeze v0

Status: frozen evidence-workstation milestone

Blueprint 8 closes the TOM v3 Visual Evidence Platform as a coherent replay evidence workstation.
It is a candidate-evidence milestone, not a truth or adjudication milestone.

## Scope

Blueprint 8 brings the replay workstation from raw visual evidence into a reproducible point-review
workflow:

```text
real detections
-> smoothed motion candidates
-> court projection candidates
-> ball trajectory court candidates
-> hit/bounce event candidates
-> marker-level arbitration
-> replay marker inspector
-> event candidate review panel
-> point evidence snapshot
```

The frozen workstation supports:

- video replay
- persisted detection overlays
- smoothed ball, player-box, and pose candidate overlays
- court keypoints, court lines, homography candidates, and projection diagnostics
- stable court geometry display carry-forward
- object-to-court projection candidates on a normalized mini-map
- ball trajectory candidate paths on the mini-map
- final `HIT CANDIDATE` and `BOUNCE CANDIDATE` video and mini-map markers
- marker-level arbitration metadata
- ordered Event Candidate Review panel rows
- Replay Marker Inspector evidence cards
- Point Evidence Snapshot JSON/Markdown reports

## Sample-Point Reproducibility

Current reproducibility context:

- media: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- motion smoothing run: `d6e23e3d-daee-4c12-aa11-2d17eee15b58`
- court run: `76391897-cdd1-46dc-ace1-9aaeb2c54845`
- court projection run: `82498799-490f-44df-9222-0157356c5ff7`
- ball trajectory run: `2e16f3d1-e252-497a-b688-d81890645ab7`

Build event candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-hit-bounce-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  BALL_TRAJECTORY_RUN_ID=2e16f3d1-e252-497a-b688-d81890645ab7 \
  COURT_PROJECTION_RUN_ID=82498799-490f-44df-9222-0157356c5ff7
```

Expected compact result:

- `hit_candidate`: 3
- `bounce_candidate`: 3
- `marker_summary`: 6
- `event_candidate_rejection_diagnostic`: 871

Generate a point evidence snapshot:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-point-evidence-snapshot \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=<fresh_event_candidate_run_id>
```

Expected snapshot result:

- `snapshot_type`: `point_evidence_snapshot`
- `snapshot_version`: `v0`
- `marker_summary`: 6
- `hit_candidate`: 3
- `bounce_candidate`: 3
- replay URL present
- source run ids present
- active versions present
- candidate-only warnings present
- known limitations present

## Operator Workflow

1. Build or obtain the source perception, court, smoothing, projection, and trajectory runs.
2. Run `make tom-v1-hit-bounce-candidates` to create current candidate markers.
3. Open the replay URL in operator view.
4. Review visible markers in the video overlay and court mini-map.
5. Use the Event Candidate Review panel to step through final visible markers in sequence.
6. Click a marker or review row to seek replay and populate the Replay Marker Inspector.
7. Inspect source method, confidence, coordinates, marker-level arbitration, and candidate warnings.
8. Run `make tom-v1-point-evidence-snapshot` for a compact JSON or Markdown point report.

## Boundary

Blueprint 8 remains candidate evidence only.

It does not add:

- hit truth
- bounce truth
- in/out decisions
- score
- rally or point truth
- player identity
- server/receiver logic
- accepted/rejected lifecycle
- manual correction workflow
- adjudication

Raw and derived observations remain immutable source evidence. The Replay Marker Inspector, Event
Candidate Review panel, marker summaries, and snapshots help operators review evidence; they do not
promote evidence to truth.

## Known Limitations

- Candidate markers are not truth.
- Hit/bounce classification remains heuristic and sample-dependent.
- Marker correctness remains operator-reviewed.
- No in/out decision exists.
- No score, point winner, or rally state exists.
- No accepted/rejected lifecycle exists.
- No manual correction workflow exists yet.
- No multi-point or match-level event timeline exists yet.
- No benchmark set or dataset-level recall/precision report exists yet.
- Court projection and homography remain candidate geometry, not court truth.
- Image-space and court-template motion diagnostics are proxies, not true 3D ball physics.

## Next Blueprint Options

Option A - Manual Candidate Review / Correction v0:
operator can flag candidate markers as useful, wrong, or unclear, while still avoiding truth
promotion.

Option B - Multi-Point Evidence Session v0:
move from one sample point to a sequence of points or media segments.

Option C - Benchmark Dataset / Evaluation Harness v0:
create a small expected-observation set for measuring candidate recall and precision.

Option D - Evidence Export Package v0:
bundle snapshot JSON/Markdown, replay URL, marker summary, and selected frame thumbnails.

Option E - Truth Promotion Design Blueprint:
design, but do not implement, how candidate evidence could later become accepted observations.

## Freeze Verdict

Blueprint 8 is ready to freeze as the Visual Evidence Platform / replay evidence workstation
milestone. The current stack is coherent, reproducible on the sample point, documented, and
candidate-only. Future work should begin as a new blueprint or explicitly scoped repair.
