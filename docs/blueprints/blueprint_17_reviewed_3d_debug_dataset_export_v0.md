# Blueprint 17 Reviewed 3D Debug Dataset Export v0

Blueprint 17 exports reviewed 3D debug evidence into deterministic offline dataset artifacts.

The export consumes existing media, event candidate, camera geometry, 3D trajectory candidate,
3D diagnostic, event-marker review, and 3D debug review rows. It writes JSON or Markdown for
offline analysis, QA review, dataset curation, and future training preparation.

The export is read-only. It does not mutate event candidates, marker arbitration, 3D candidates,
3D diagnostics, review annotations, in/out, score, point state, accepted/rejected lifecycle, or
adjudication.

## Command

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli export-reviewed-3d-debug-dataset \
  --media-id <media_id> \
  --event-candidate-run-id <event_candidate_run_id> \
  --trajectory-3d-run-id <trajectory_3d_run_id> \
  --camera-geometry-id <camera_geometry_id> \
  --format json \
  --output .data/exports/reviewed_3d_debug_dataset.json
```

Make helper:

```bash
make tom-v1-export-reviewed-3d-debug-dataset \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id> \
  FORMAT=json \
  OUTPUT=.data/exports/reviewed_3d_debug_dataset.json
```

## Output

JSON includes:

- media, event-candidate run, 3D trajectory run, and camera geometry IDs
- replay URL
- camera geometry summary
- 3D trajectory candidate summary
- event marker summary with review context
- compact 3D candidate rows
- compact event-candidate 3D diagnostic rows
- 3D debug review annotations
- event candidate review annotations
- warnings and limitations

Markdown includes IDs, replay URL, summary tables, warnings, event markers, 3D summary sections,
compact candidate examples, and known limitations.

## Boundaries

Export labels are `review_metadata_only` and `operator_reviewed_only` context. They are not truth,
not 3D truth, and not training truth. Height remains unknown unless future evidence says otherwise.
The export does not create confirmed hits, confirmed bounces, in/out, score, player identity, or
adjudication.
