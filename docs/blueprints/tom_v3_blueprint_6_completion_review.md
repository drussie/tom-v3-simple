# TOM v3 Blueprint 6 Completion Review

Date: 2026-05-27

Status: COMPLETE

## Completion Verdict

Blueprint 6 is complete enough to stop.

TOM v3 now has a usable visual replay/operator workstation on top of the completed local observation platform. It can open indexed local video, play it in Replay Mode or Stream Proxy Mode, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, and support click-to-seek and click-to-select persisted evidence.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, websocket live updates, live model scheduling, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

## What Blueprint 6 Proves

```text
indexed media
-> browser video playback
-> media-owned frame/time synchronization
-> Replay Mode
-> persisted detection observation overlays
-> persisted tracklet candidate overlays
-> persisted pose keypoint overlays
-> evidence timeline lanes
-> click-to-seek evidence
-> click-to-select persisted observations
-> Stream Proxy Mode
-> hidden future evidence until the live-like proxy edge reaches it
```

## Completion Questions

1. Is Blueprint 6 complete enough to stop?
   Yes. The replay/operator workstation foundation is complete for indexed local media and persisted TOM evidence.

2. What does the replay workstation do now?
   It plays indexed video, maps playback time to TOM frame/time, renders synchronized persisted evidence overlays, shows timeline lanes, and lets the operator select evidence from overlays or timeline items.

3. What does Replay Mode support?
   Replay Mode supports free review of the indexed video, synchronized detection/tracklet/pose overlays, run selection, timeline lanes, click-to-seek, and click-to-select evidence details.

4. What does Stream Proxy Mode support?
   Stream Proxy Mode treats indexed local video as a video-as-live source, starts at the beginning, advances a live-like edge, hides future evidence until it becomes available, shows available evidence counts and lag/review state, and supports return-to-live-edge.

5. Can the user watch video with TOM detection overlays?
   Yes. Persisted `ball_detection` and `player_detection` observations render as synchronized bbox overlays.

6. Can the user watch candidate tracklet overlays?
   Yes. Persisted tracklet candidates and track point candidates render as synchronized points and selected candidate paths.

7. Can the user watch pose keypoint/skeleton overlays?
   Yes. Persisted pose observations render present keypoints and skeleton edges without drawing missing keypoints as present evidence.

8. Can the user navigate with timeline lanes?
   Yes. The replay timeline includes detection observation ticks, tracklet candidate spans, pose observation ticks, and review annotation markers.

9. Can the user click timeline items to seek/select evidence?
   Yes. Timeline items seek the video and select the corresponding persisted evidence detail.

10. Can the user click overlays to inspect persisted evidence?
    Yes. Detection, tracklet, track point, and pose overlays populate selected evidence detail in the replay workstation.

11. Does Stream Proxy Mode hide future evidence until the proxy live edge reaches it?
    Yes. Future overlays and timeline items are hidden or clipped until the live-like proxy edge reaches their media-owned time.

12. Does Blueprint 6 add real live ingestion?
    No. Stream Proxy Mode is a UI/operator behavior over indexed local files and already-persisted observations.

13. Does Blueprint 6 add tennis-event interpretation?
    No. It displays synchronized evidence only.

14. Are limitations explicit?
    Yes. `docs/KNOWN_LIMITATIONS.md`, `docs/REPLAY_WORKSTATION.md`, and the control-room docs separate the replay workstation from real stream ingestion and tennis intelligence.

15. What future work should be separate from Blueprint 6?
    Real live ingestion, real pose runtime, homography/court-space evidence, bounce/hit candidate evidence, movement/stroke evidence candidates, and product deployment should start as new blueprints if deliberately chosen.

## Replay Mode Final Smoke

Replay Mode expected behavior:

- indexed video loads in `/replay/<media_id>`
- current media timestamp and nearest TOM frame update during playback
- detection observation overlays render
- tracklet candidate overlays render
- pose keypoint overlays render
- evidence timeline lanes render
- clicking timeline items seeks/selects evidence
- clicking overlays selects persisted evidence detail
- no tennis-event interpretation is displayed

## Stream Proxy Mode Final Smoke

Stream Proxy Mode expected behavior:

- `mode=stream_proxy` is visible in the workstation
- playback starts at the beginning as a video-as-live proxy
- future timeline evidence is hidden until the live-like edge reaches it
- future overlays are hidden until the live-like edge reaches them
- available evidence counts, lag/review state, and return-to-live-edge are visible
- no real live stream ingestion is created
- no tennis-event interpretation is displayed

## Known Limitations Preserved

- Local indexed file playback only.
- Stream Proxy Mode is not real live ingestion.
- Persisted observations already exist before Stream Proxy Mode hides future UI evidence.
- No HLS, RTSP, HDMI, webcam, capture-card, frame-buffer, or websocket stream infrastructure.
- No real pose inference.
- No movement/stroke interpretation.
- No homography or court-space reasoning.
- No bounce/hit/rally/point/scoring.
- No TOM v2-style adjudication.

## Future Blueprint Candidates

- Blueprint 7 - Real Live Stream Ingestion
- Blueprint 7 - Real Pose Runtime
- Blueprint 7 - Homography / Court-Space Evidence
- Blueprint 7 - Bounce / Hit Candidate Evidence
- Blueprint 7 - Movement / Stroke Evidence Candidates
- Product Deployment Blueprint

Do not choose one automatically as part of Blueprint 6. Blueprint 6 is closed.
