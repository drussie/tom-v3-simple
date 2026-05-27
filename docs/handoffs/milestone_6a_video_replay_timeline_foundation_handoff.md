# Milestone 6A Handoff - Video Replay Timeline Foundation

## Status

Milestone 6A is complete.

Blueprint 6 has started as the visual replay/operator layer after TOM v3 Simple completion.

## What Was Added

- `GET /media/{media_id}/replay-info`
- `GET /media/{media_id}/video`
- replay frame/time mapping helpers in `apps/api/services/replay.py`
- `/replay/[mediaId]` frontend route
- `ReplayVideoPlayer` component
- basic replay timeline/progress shell
- selected run context display
- available run grouping by evidence type
- `make replay-open MEDIA_ID=<media_id>`
- `docs/REPLAY_WORKSTATION.md`

## What 6A Proves

A user can open an indexed local media asset in the replay workstation, play the video, and see the current media-owned timestamp and nearest frame update from indexed metadata.

## What 6A Does Not Prove

6A does not draw detection, tracklet, or pose overlays during playback. It does not add live stream ingestion or any tennis-event interpretation.

## Main Local Smoke

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
```

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db \
make completion-audit PYTHON=.venv/bin/python
```

Start API and web:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db \
.venv/bin/python -m uvicorn apps.api.main:app --reload
```

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/replay/<media_id>
```

## Next Recommended Milestone

Milestone 6B - Detection Overlay Playback

6B should draw persisted detection observations over video playback using the 6A frame/time foundation.
