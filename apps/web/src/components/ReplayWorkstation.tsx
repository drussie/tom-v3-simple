"use client";

import type { ReactNode } from "react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { fetchReplayOverlayChunk, fetchReplayTimeline } from "../lib/api";
import {
  filterDetectionsAvailableAt,
  filterPosesAvailableAt,
  filterTrackletsAvailableAt,
  selectInitialReplayRun
} from "../lib/replayOverlays";
import { formatReplayTime } from "../lib/replayTime";
import {
  timelineAvailableItemCount,
  timelineItemKey,
  timelineItemTimestampMs
} from "../lib/replayTimeline";
import type {
  ReplayDetectionOverlay,
  ReplayInfo,
  ReplayMode,
  ReplayOverlayChunk,
  ReplayPlaybackState,
  ReplayPoseOverlay,
  ReplayRunSummary,
  ReplaySeekRequest,
  ReplayTimeline,
  ReplayTimelineItem,
  ReplayTrackletOverlay,
  ReplayTrackPointOverlay
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";
import { ReplayDetectionOverlay as ReplayDetectionOverlayLayer } from "./ReplayDetectionOverlay";
import { ReplayEvidenceTimeline } from "./ReplayEvidenceTimeline";
import { ReplayPoseOverlay as ReplayPoseOverlayLayer } from "./ReplayPoseOverlay";
import { ReplayTrackletOverlay as ReplayTrackletOverlayLayer } from "./ReplayTrackletOverlay";
import { ReplayVideoPlayer } from "./ReplayVideoPlayer";

const overlayChunkMs = 2000;

interface ReplayWorkstationProps {
  initialMode?: ReplayMode;
  replayInfo: ReplayInfo;
  selectedRuns: {
    detectionRunId?: string;
    trackletRunId?: string;
    poseRunId?: string;
  };
}

interface OverlayState {
  chunk: ReplayOverlayChunk | null;
  loading: boolean;
  error: string | null;
}

interface TimelineState {
  timeline: ReplayTimeline | null;
  loading: boolean;
  error: string | null;
}

type SelectedReplayEvidence =
  | { kind: "detection"; detection: ReplayDetectionOverlay }
  | { kind: "detection_timeline"; item: Extract<ReplayTimelineItem, { item_type: "detection" }> }
  | { kind: "tracklet"; tracklet: ReplayTrackletOverlay }
  | { kind: "tracklet_timeline"; item: Extract<ReplayTimelineItem, { item_type: "tracklet" }> }
  | { kind: "track_point"; tracklet: ReplayTrackletOverlay; point: ReplayTrackPointOverlay }
  | { kind: "pose"; pose: ReplayPoseOverlay }
  | { kind: "pose_timeline"; item: Extract<ReplayTimelineItem, { item_type: "pose" }> }
  | { kind: "annotation"; item: Extract<ReplayTimelineItem, { item_type: "annotation" }> };

export function ReplayWorkstation({
  initialMode = "replay",
  replayInfo,
  selectedRuns
}: ReplayWorkstationProps) {
  const initialDetectionRunId = useMemo(
    () => selectInitialReplayRun(replayInfo.available_runs.detection, selectedRuns.detectionRunId),
    [replayInfo.available_runs.detection, selectedRuns.detectionRunId]
  );
  const initialTrackletRunId = useMemo(
    () => selectInitialReplayRun(replayInfo.available_runs.tracklet, selectedRuns.trackletRunId),
    [replayInfo.available_runs.tracklet, selectedRuns.trackletRunId]
  );
  const initialPoseRunId = useMemo(
    () => selectInitialReplayRun(replayInfo.available_runs.pose, selectedRuns.poseRunId),
    [replayInfo.available_runs.pose, selectedRuns.poseRunId]
  );

  const [selectedDetectionRunId, setSelectedDetectionRunId] = useState<string | null>(
    initialDetectionRunId
  );
  const [selectedTrackletRunId, setSelectedTrackletRunId] = useState<string | null>(
    initialTrackletRunId
  );
  const [selectedPoseRunId, setSelectedPoseRunId] = useState<string | null>(initialPoseRunId);
  const [showDetections, setShowDetections] = useState(true);
  const [showTracklets, setShowTracklets] = useState(true);
  const [showPoses, setShowPoses] = useState(true);
  const [replayMode, setReplayMode] = useState<ReplayMode>(initialMode);
  const [streamLiveEdgeMs, setStreamLiveEdgeMs] = useState(0);
  const [streamProxyNotice, setStreamProxyNotice] = useState<string | null>(null);
  const [selectedEvidence, setSelectedEvidence] = useState<SelectedReplayEvidence | null>(null);
  const [playback, setPlayback] = useState<ReplayPlaybackState>({
    currentTimeSeconds: 0,
    timestampMs: 0,
    frameNumber: 0,
    durationSeconds: replayInfo.duration_ms !== null ? replayInfo.duration_ms / 1000 : 0,
    paused: true
  });
  const [overlayState, setOverlayState] = useState<OverlayState>({
    chunk: null,
    loading: false,
    error: null
  });
  const [timelineState, setTimelineState] = useState<TimelineState>({
    timeline: null,
    loading: false,
    error: null
  });
  const [seekRequest, setSeekRequest] = useState<ReplaySeekRequest | null>(null);
  const chunkCache = useRef<Map<string, ReplayOverlayChunk>>(new Map());

  useEffect(() => {
    setSelectedDetectionRunId(initialDetectionRunId);
  }, [initialDetectionRunId]);

  useEffect(() => {
    setSelectedTrackletRunId(initialTrackletRunId);
  }, [initialTrackletRunId]);

  useEffect(() => {
    setSelectedPoseRunId(initialPoseRunId);
  }, [initialPoseRunId]);

  useEffect(() => {
    setReplayMode(initialMode);
  }, [initialMode]);

  useEffect(() => {
    if (replayMode === "stream_proxy") {
      setStreamLiveEdgeMs(0);
      setStreamProxyNotice(null);
      setSelectedEvidence(null);
      setSeekRequest({ timestampMs: 0, nonce: Date.now() });
      chunkCache.current.clear();
      return;
    }
    setStreamProxyNotice(null);
  }, [replayMode]);

  const enabledLayers = useMemo(() => {
    const layers: string[] = [];
    if (showDetections && selectedDetectionRunId !== null) {
      layers.push("detections");
    }
    if (showTracklets && selectedTrackletRunId !== null) {
      layers.push("tracklets");
    }
    if (showPoses && selectedPoseRunId !== null) {
      layers.push("pose");
    }
    return layers;
  }, [
    selectedDetectionRunId,
    selectedPoseRunId,
    selectedTrackletRunId,
    showDetections,
    showPoses,
    showTracklets
  ]);

  const currentChunkStart = Math.floor(playback.timestampMs / overlayChunkMs) * overlayChunkMs;
  const currentChunkEnd = currentChunkStart + overlayChunkMs;
  const layersParam = enabledLayers.join(",");
  const chunkKey = [
    replayInfo.media_id,
    selectedDetectionRunId ?? "none",
    selectedTrackletRunId ?? "none",
    selectedPoseRunId ?? "none",
    layersParam || "none",
    currentChunkStart,
    currentChunkEnd
  ].join(":");

  useEffect(() => {
    if (enabledLayers.length === 0) {
      setOverlayState({ chunk: null, loading: false, error: null });
      return;
    }

    const cached = chunkCache.current.get(chunkKey);
    if (cached !== undefined) {
      setOverlayState({ chunk: cached, loading: false, error: null });
      return;
    }

    let cancelled = false;
    setOverlayState((current) => ({ ...current, loading: true, error: null }));
    fetchReplayOverlayChunk({
      mediaId: replayInfo.media_id,
      startMs: currentChunkStart,
      endMs: currentChunkEnd,
      detectionRunId: selectedDetectionRunId,
      trackletRunId: selectedTrackletRunId,
      poseRunId: selectedPoseRunId,
      layers: layersParam
    })
      .then((chunk) => {
        if (!cancelled) {
          chunkCache.current.set(chunkKey, chunk);
          setOverlayState({ chunk, loading: false, error: null });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setOverlayState({
            chunk: null,
            loading: false,
            error: error instanceof Error ? error.message : "Unable to load replay overlays"
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [
    chunkKey,
    currentChunkEnd,
    currentChunkStart,
    enabledLayers.length,
    layersParam,
    replayInfo.media_id,
    selectedDetectionRunId,
    selectedPoseRunId,
    selectedTrackletRunId
  ]);

  useEffect(() => {
    let cancelled = false;
    setTimelineState((current) => ({ ...current, loading: true, error: null }));
    fetchReplayTimeline({
      mediaId: replayInfo.media_id,
      detectionRunId: selectedDetectionRunId,
      trackletRunId: selectedTrackletRunId,
      poseRunId: selectedPoseRunId,
      includeAnnotations: true
    })
      .then((timeline) => {
        if (!cancelled) {
          setTimelineState({ timeline, loading: false, error: null });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setTimelineState({
            timeline: null,
            loading: false,
            error: error instanceof Error ? error.message : "Unable to load replay timeline"
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [replayInfo.media_id, selectedDetectionRunId, selectedPoseRunId, selectedTrackletRunId]);

  const handlePlaybackStateChange = useCallback(
    (state: ReplayPlaybackState) => {
      setPlayback(state);
      if (replayMode === "stream_proxy") {
        const durationMs =
          replayInfo.duration_ms ?? Math.max(0, Math.round(state.durationSeconds * 1000));
        setStreamLiveEdgeMs((current) =>
          Math.min(durationMs, Math.max(current, state.timestampMs))
        );
      }
    },
    [replayInfo.duration_ms, replayMode]
  );

  const handleTimelineItemSelect = useCallback(
    (item: ReplayTimelineItem) => {
      const targetTimestampMs = timelineItemTimestampMs(item);
      if (replayMode === "stream_proxy" && targetTimestampMs > streamLiveEdgeMs) {
        setStreamProxyNotice(
          "Future evidence is hidden until Stream Proxy Mode reaches that media time."
        );
        setSeekRequest({ timestampMs: streamLiveEdgeMs, nonce: Date.now() });
        return;
      }
      setSeekRequest({ timestampMs: targetTimestampMs, nonce: Date.now() });
      if (item.item_type === "detection") {
        setSelectedEvidence({ kind: "detection_timeline", item });
        return;
      }
      if (item.item_type === "tracklet") {
        setSelectedEvidence({ kind: "tracklet_timeline", item });
        return;
      }
      if (item.item_type === "pose") {
        setSelectedEvidence({ kind: "pose_timeline", item });
        return;
      }
      setSelectedEvidence({ kind: "annotation", item });
    },
    [replayMode, streamLiveEdgeMs]
  );

  const streamAvailableUntilMs = replayMode === "stream_proxy" ? streamLiveEdgeMs : null;
  const detections = filterDetectionsAvailableAt(
    overlayState.chunk?.detections ?? [],
    streamAvailableUntilMs
  );
  const tracklets = filterTrackletsAvailableAt(
    overlayState.chunk?.tracklets ?? [],
    streamAvailableUntilMs
  );
  const poses = filterPosesAvailableAt(overlayState.chunk?.poses ?? [], streamAvailableUntilMs);
  const totalTimelineItemCount = useMemo(
    () =>
      timelineState.timeline?.lanes.reduce((count, lane) => count + lane.items.length, 0) ?? 0,
    [timelineState.timeline]
  );
  const availableTimelineItemCount = useMemo(
    () =>
      timelineState.timeline !== null
        ? timelineAvailableItemCount(timelineState.timeline.lanes, streamAvailableUntilMs)
        : 0,
    [streamAvailableUntilMs, timelineState.timeline]
  );
  const handleReturnToLiveEdge = useCallback(() => {
    setSeekRequest({ timestampMs: streamLiveEdgeMs, nonce: Date.now() });
  }, [streamLiveEdgeMs]);
  const handleSeekPastLiveEdge = useCallback(() => {
    setStreamProxyNotice("Stream Proxy Mode cannot seek beyond the current live-like edge.");
  }, []);
  const selectedDetectionId =
    selectedEvidence?.kind === "detection"
      ? selectedEvidence.detection.observation_id
      : selectedEvidence?.kind === "detection_timeline"
        ? selectedEvidence.item.observation_id
        : null;
  const selectedTrackletId =
    selectedEvidence?.kind === "tracklet"
      ? selectedEvidence.tracklet.tracklet_id
      : selectedEvidence?.kind === "tracklet_timeline"
        ? selectedEvidence.item.tracklet_id
      : selectedEvidence?.kind === "track_point"
        ? selectedEvidence.tracklet.tracklet_id
        : null;
  const selectedTrackPointId =
    selectedEvidence?.kind === "track_point" ? selectedEvidence.point.track_point_id : null;
  const selectedPoseObservationId =
    selectedEvidence?.kind === "pose"
      ? selectedEvidence.pose.observation_id
      : selectedEvidence?.kind === "pose_timeline"
        ? selectedEvidence.item.observation_id
        : null;
  const selectedTimelineKey = selectedTimelineItemKey(selectedEvidence);

  return (
    <main className="viewer-shell replay-shell">
      <header className="viewer-header">
        <div className="viewer-title">
          <p className="eyebrow">TOM v3 Replay Workstation</p>
          <h1>Replay and Stream Proxy workstation</h1>
          <div className="meta-line">
            <span className="status-pill">observation-only</span>
            <span className="mini-pill">no adjudication</span>
            <span className="mini-pill">
              {replayMode === "stream_proxy" ? "Stream Proxy Mode" : "Replay Mode"}
            </span>
            <span className="mono">{replayInfo.media_id}</span>
          </div>
        </div>
        <div className="meta-line">
          <span className="mini-pill">{replayInfo.frame_time_mode} frame/time</span>
          <span className="mini-pill">{detections.length} detection overlays</span>
          <span className="mini-pill">{tracklets.length} tracklet candidates</span>
          <span className="mini-pill">{poses.length} pose observations</span>
        </div>
      </header>

      <div className="replay-grid">
        <div className="main-column">
          <ReplayVideoPlayer
            onPlaybackStateChange={handlePlaybackStateChange}
            onSeekPastLiveEdge={handleSeekPastLiveEdge}
            replayInfo={replayInfo}
            seekRequest={seekRequest}
            streamLiveEdgeMs={streamAvailableUntilMs}
            streamProxyMode={replayMode === "stream_proxy"}
          >
            <ReplayDetectionOverlayLayer
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              detections={detections}
              enabled={showDetections && selectedDetectionRunId !== null}
              error={overlayState.error}
              isLoading={overlayState.loading}
              onSelectObservation={(detection) => {
                setSelectedEvidence({ kind: "detection", detection });
              }}
              replayInfo={replayInfo}
              selectedObservationId={selectedDetectionId}
            />
            <ReplayTrackletOverlayLayer
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              enabled={showTracklets && selectedTrackletRunId !== null}
              error={overlayState.error}
              isLoading={overlayState.loading}
              onSelectTracklet={(tracklet) => {
                setSelectedEvidence({ kind: "tracklet", tracklet });
              }}
              onSelectTrackPoint={(tracklet, point) => {
                setSelectedEvidence({ kind: "track_point", tracklet, point });
              }}
              replayInfo={replayInfo}
              selectedTrackletId={selectedTrackletId}
              selectedTrackPointId={selectedTrackPointId}
              tracklets={tracklets}
            />
            <ReplayPoseOverlayLayer
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              enabled={showPoses && selectedPoseRunId !== null}
              error={overlayState.error}
              isLoading={overlayState.loading}
              onSelectPose={(pose) => {
                setSelectedEvidence({ kind: "pose", pose });
              }}
              poses={poses}
              replayInfo={replayInfo}
              selectedObservationId={selectedPoseObservationId}
            />
          </ReplayVideoPlayer>
          <ReplayModeControls
            availableTimelineItemCount={availableTimelineItemCount}
            durationMs={replayInfo.duration_ms ?? Math.round(playback.durationSeconds * 1000)}
            onModeChange={setReplayMode}
            onReturnToLiveEdge={handleReturnToLiveEdge}
            playback={playback}
            replayMode={replayMode}
            streamLiveEdgeMs={streamLiveEdgeMs}
            streamProxyNotice={streamProxyNotice}
            totalTimelineItemCount={totalTimelineItemCount}
          />
          <ReplayLayerControls
            detectionRuns={replayInfo.available_runs.detection}
            onSelectedDetectionRunChange={(runId) => {
              setSelectedDetectionRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedPoseRunChange={(runId) => {
              setSelectedPoseRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedTrackletRunChange={(runId) => {
              setSelectedTrackletRunId(runId);
              setSelectedEvidence(null);
            }}
            onToggleDetections={setShowDetections}
            onTogglePoses={setShowPoses}
            onToggleTracklets={setShowTracklets}
            poseRuns={replayInfo.available_runs.pose}
            selectedDetectionRunId={selectedDetectionRunId}
            selectedPoseRunId={selectedPoseRunId}
            selectedTrackletRunId={selectedTrackletRunId}
            showDetections={showDetections}
            showPoses={showPoses}
            showTracklets={showTracklets}
            trackletRuns={replayInfo.available_runs.tracklet}
          />
          <ReplayEvidenceTimeline
            availableUntilMs={streamAvailableUntilMs}
            currentTimestampMs={playback.timestampMs}
            durationMs={replayInfo.duration_ms}
            error={timelineState.error}
            isLoading={timelineState.loading}
            layerVisibility={{
              detections: showDetections,
              tracklets: showTracklets,
              pose: showPoses,
              annotations: true
            }}
            onSelectItem={handleTimelineItemSelect}
            selectedItemKey={selectedTimelineKey}
            timeline={timelineState.timeline}
          />
          <SelectedRunContext
            replayInfo={replayInfo}
            selectedDetectionRunId={selectedDetectionRunId}
            selectedPoseRunId={selectedPoseRunId}
            selectedTrackletRunId={selectedTrackletRunId}
          />
        </div>
        <aside className="side-column">
          <ReplayMediaPanel replayInfo={replayInfo} />
          <SelectedEvidencePanel selectedEvidence={selectedEvidence} />
          <AvailableRunsPanel replayInfo={replayInfo} />
        </aside>
      </div>
    </main>
  );
}

function ReplayModeControls({
  availableTimelineItemCount,
  durationMs,
  onModeChange,
  onReturnToLiveEdge,
  playback,
  replayMode,
  streamLiveEdgeMs,
  streamProxyNotice,
  totalTimelineItemCount
}: {
  availableTimelineItemCount: number;
  durationMs: number | null;
  onModeChange: (mode: ReplayMode) => void;
  onReturnToLiveEdge: () => void;
  playback: ReplayPlaybackState;
  replayMode: ReplayMode;
  streamLiveEdgeMs: number;
  streamProxyNotice: string | null;
  totalTimelineItemCount: number;
}) {
  const isStreamProxy = replayMode === "stream_proxy";
  const lagMs = Math.max(0, streamLiveEdgeMs - playback.timestampMs);
  const atLiveEdge = !isStreamProxy || lagMs <= 250;
  const durationLabel = durationMs !== null ? formatReplayTime(durationMs / 1000) : "n/a";

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Replay Mode</h2>
        <span className="mini-pill">{isStreamProxy ? "video-as-live" : "free review"}</span>
      </div>
      <div className="panel-body replay-mode-panel">
        <div className="replay-mode-switch" role="group" aria-label="Replay mode">
          <button
            aria-pressed={replayMode === "replay"}
            className={replayMode === "replay" ? "selected" : ""}
            onClick={() => onModeChange("replay")}
            type="button"
          >
            Replay Mode
          </button>
          <button
            aria-pressed={isStreamProxy}
            className={isStreamProxy ? "selected" : ""}
            onClick={() => onModeChange("stream_proxy")}
            type="button"
          >
            Stream Proxy Mode
          </button>
        </div>
        {isStreamProxy ? (
          <>
            <div className="stream-proxy-status-grid">
              <TelemetryLikeCell label="live edge" value={formatReplayTime(streamLiveEdgeMs / 1000)} />
              <TelemetryLikeCell label="operator time" value={formatReplayTime(playback.currentTimeSeconds)} />
              <TelemetryLikeCell label="lag" value={formatReplayTime(lagMs / 1000)} />
              <TelemetryLikeCell label="duration" value={durationLabel} />
              <TelemetryLikeCell
                label="available evidence"
                value={`${availableTimelineItemCount} / ${totalTimelineItemCount}`}
              />
              <TelemetryLikeCell label="state" value={playback.paused ? "paused review" : "playing"} />
            </div>
            <div className="meta-line">
              <span className={atLiveEdge ? "status-pill" : "mini-pill"}>
                {atLiveEdge ? "at live edge" : "reviewing behind live edge"}
              </span>
              <button
                className="quiet-button"
                disabled={atLiveEdge}
                onClick={onReturnToLiveEdge}
                type="button"
              >
                Return to live edge
              </button>
            </div>
            {streamProxyNotice !== null ? (
              <p className="empty-state compact">{streamProxyNotice}</p>
            ) : null}
            <p className="evidence-note">
              Stream Proxy Mode uses the indexed video as a live-like source. Future overlays and
              timeline items stay hidden until playback reaches their media-owned time.
            </p>
          </>
        ) : (
          <p className="evidence-note">
            Replay Mode is post-run review: the operator can scrub freely and inspect the full
            persisted evidence timeline.
          </p>
        )}
      </div>
    </section>
  );
}

function ReplayLayerControls({
  detectionRuns,
  trackletRuns,
  poseRuns,
  selectedDetectionRunId,
  selectedTrackletRunId,
  selectedPoseRunId,
  showDetections,
  showTracklets,
  showPoses,
  onSelectedDetectionRunChange,
  onSelectedTrackletRunChange,
  onSelectedPoseRunChange,
  onToggleDetections,
  onToggleTracklets,
  onTogglePoses
}: {
  detectionRuns: ReplayRunSummary[];
  trackletRuns: ReplayRunSummary[];
  poseRuns: ReplayRunSummary[];
  selectedDetectionRunId: string | null;
  selectedTrackletRunId: string | null;
  selectedPoseRunId: string | null;
  showDetections: boolean;
  showTracklets: boolean;
  showPoses: boolean;
  onSelectedDetectionRunChange: (runId: string | null) => void;
  onSelectedTrackletRunChange: (runId: string | null) => void;
  onSelectedPoseRunChange: (runId: string | null) => void;
  onToggleDetections: (enabled: boolean) => void;
  onToggleTracklets: (enabled: boolean) => void;
  onTogglePoses: (enabled: boolean) => void;
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Replay Overlay Layers</h2>
        <span className="mini-pill">persisted evidence</span>
      </div>
      <div className="panel-body replay-controls">
        <LayerToggle
          checked={showDetections}
          label="Show detection observations"
          onChange={onToggleDetections}
        />
        <RunSelect
          label="Detection run"
          onChange={onSelectedDetectionRunChange}
          runs={detectionRuns}
          selectedRunId={selectedDetectionRunId}
        />
        <LayerToggle
          checked={showTracklets}
          label="Show tracklet candidates"
          onChange={onToggleTracklets}
        />
        <RunSelect
          label="Tracklet run"
          onChange={onSelectedTrackletRunChange}
          runs={trackletRuns}
          selectedRunId={selectedTrackletRunId}
        />
        <LayerToggle
          checked={showPoses}
          label="Show pose observations"
          onChange={onTogglePoses}
        />
        <RunSelect
          label="Pose run"
          onChange={onSelectedPoseRunChange}
          runs={poseRuns}
          selectedRunId={selectedPoseRunId}
        />
        <p className="evidence-note">
          Overlays are synchronized persisted evidence. Display holds make sparse fixture output
          inspectable but do not alter stored observations.
        </p>
      </div>
    </section>
  );
}

function LayerToggle({
  checked,
  label,
  onChange
}: {
  checked: boolean;
  label: string;
  onChange: (enabled: boolean) => void;
}) {
  return (
    <label className="toggle-row">
      <input checked={checked} onChange={(event) => onChange(event.target.checked)} type="checkbox" />
      <span>{label}</span>
    </label>
  );
}

function RunSelect({
  label,
  runs,
  selectedRunId,
  onChange
}: {
  label: string;
  runs: ReplayRunSummary[];
  selectedRunId: string | null;
  onChange: (runId: string | null) => void;
}) {
  return (
    <label className="select-row">
      <span>{label}</span>
      <select onChange={(event) => onChange(event.target.value || null)} value={selectedRunId ?? ""}>
        <option value="">Select a run</option>
        {runs.map((run) => (
          <option key={run.run_id} value={run.run_id}>
            {formatReplayRunOptionLabel(run)}
          </option>
        ))}
      </select>
    </label>
  );
}

function ReplayMediaPanel({ replayInfo }: { replayInfo: ReplayInfo }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Media</h2>
        <span className="mini-pill">indexed video</span>
      </div>
      <div className="panel-body replay-media-detail">
        <DetailRow label="media id" value={replayInfo.media_id} />
        <DetailRow label="source" value={replayInfo.source_uri} />
        <DetailRow
          label="dimensions"
          value={`${replayInfo.width ?? "n/a"} x ${replayInfo.height ?? "n/a"}`}
        />
        <DetailRow label="duration_ms" value={replayInfo.duration_ms?.toString() ?? "n/a"} />
        <DetailRow label="fps" value={replayInfo.fps?.toString() ?? "n/a"} />
        <DetailRow label="frame_count" value={replayInfo.frame_count?.toString() ?? "n/a"} />
        <DetailRow label="video endpoint" value={replayInfo.video_url} />
      </div>
    </section>
  );
}

function AvailableRunsPanel({ replayInfo }: { replayInfo: ReplayInfo }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Available Run Context</h2>
        <span className="mini-pill">persisted evidence</span>
      </div>
      <div className="panel-body run-group-list">
        <RunGroup title="Detection observations" runs={replayInfo.available_runs.detection} />
        <RunGroup title="Tracklet candidates" runs={replayInfo.available_runs.tracklet} />
        <RunGroup title="Pose observations" runs={replayInfo.available_runs.pose} />
        <RunGroup
          title="Gameplay/view-state observations"
          runs={replayInfo.available_runs.gameplay}
        />
      </div>
    </section>
  );
}

function SelectedRunContext({
  replayInfo,
  selectedDetectionRunId,
  selectedTrackletRunId,
  selectedPoseRunId
}: {
  replayInfo: ReplayInfo;
  selectedDetectionRunId: string | null;
  selectedTrackletRunId: string | null;
  selectedPoseRunId: string | null;
}) {
  const selected = [
    ["detection", selectedDetectionRunId, replayInfo.available_runs.detection],
    ["tracklet candidate", selectedTrackletRunId, replayInfo.available_runs.tracklet],
    ["pose observation", selectedPoseRunId, replayInfo.available_runs.pose]
  ] as const;

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Selected Run Context</h2>
        <span className="mini-pill">replay context</span>
      </div>
      <div className="panel-body run-group-list">
        {selected.map(([label, runId, runs]) => (
          <SelectedRunRow key={label} label={label} runId={runId ?? undefined} runs={runs} />
        ))}
        <p className="empty-state">
          Selected runs provide synchronized detection observations, tracklet candidates, and pose
          keypoint evidence. They do not confirm tennis events or object identity.
        </p>
      </div>
    </section>
  );
}

function SelectedEvidencePanel({
  selectedEvidence
}: {
  selectedEvidence: SelectedReplayEvidence | null;
}) {
  if (selectedEvidence === null) {
    return (
      <section className="panel">
        <div className="panel-header">
          <h2>Selected Evidence</h2>
          <span className="mini-pill">none</span>
        </div>
        <div className="panel-body replay-media-detail">
          <p className="empty-state">
            Click a replay bbox, track point, candidate path, or pose skeleton to inspect persisted
            evidence.
          </p>
        </div>
      </section>
    );
  }

  if (selectedEvidence.kind === "detection") {
    const { detection } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Detection Observation" badge={detection.observation_type}>
        <DetailRow label="observation id" value={detection.observation_id} />
        <DetailRow label="run id" value={detection.run_id} />
        <DetailRow label="label" value={detection.label} />
        <DetailRow label="confidence" value={formatConfidence(detection.confidence)} />
        <DetailRow label="frame" value={detection.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={detection.timestamp_ms.toString()} />
        <DetailRow
          label="bbox"
          value={`${detection.bbox.x}, ${detection.bbox.y}, ${detection.bbox.w}, ${detection.bbox.h}`}
        />
        <DetailRow label="source" value={detection.source_language} />
        <DetailRow label="evidence source" value={sourceDisplayLabel(detection)} />
        <DetailRow label="source runtime" value={detection.source_runtime ?? "n/a"} />
        <DetailRow label="model registry id" value={detection.model_registry_id ?? "n/a"} />
        <DetailRow
          label="model"
          value={formatModelNameVersion(detection.model_name, detection.model_version)}
        />
        <DetailRow label="runtime config id" value={detection.runtime_config_id ?? "n/a"} />
        <DetailRow label="class id" value={detection.class_id?.toString() ?? "n/a"} />
        <DetailRow label="class label" value={detection.class_label ?? "n/a"} />
        <DetailRow label="frame/time owner" value={detection.frame_time_owner ?? "n/a"} />
        <a className="quiet-link" href={`/runs/${detection.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          {detection.real_model_output
            ? "Real model output detection observation. Evidence only, not an object identity or tennis event conclusion."
            : "Detection observation. Evidence only, not an object identity or tennis event conclusion."}
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "detection_timeline") {
    const { item } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Detection Observation" badge={item.observation_type}>
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="label" value={item.label} />
        <DetailRow label="confidence" value={formatConfidence(item.confidence)} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="evidence source" value={sourceDisplayLabel(item)} />
        <DetailRow label="model registry id" value={item.model_registry_id ?? "n/a"} />
        <DetailRow
          label="model"
          value={formatModelNameVersion(item.model_name, item.model_version)}
        />
        <DetailRow label="runtime config id" value={item.runtime_config_id ?? "n/a"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          {item.real_model_output
            ? "Real model output detection observation selected from the evidence timeline. Evidence only, not an object identity or tennis event conclusion."
            : "Detection observation selected from the evidence timeline. Evidence only, not an object identity or tennis event conclusion."}
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "tracklet") {
    const { tracklet } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Tracklet Candidate" badge={tracklet.track_type}>
        <DetailRow label="tracklet id" value={tracklet.tracklet_id} />
        <DetailRow label="observation id" value={tracklet.observation_id ?? "n/a"} />
        <DetailRow label="run id" value={tracklet.run_id} />
        <DetailRow label="label hint" value={tracklet.label_hint ?? "n/a"} />
        <DetailRow label="track_status" value={tracklet.track_status} />
        <DetailRow label="identity_status" value={tracklet.identity_status} />
        <DetailRow
          label="source detection run"
          value={tracklet.source_detection_run_id ?? "n/a"}
        />
        <DetailRow
          label="source evidence"
          value={sourceDetectionDisplayLabel(tracklet)}
        />
        <DetailRow
          label="source runtime"
          value={tracklet.source_detection_runtime ?? "n/a"}
        />
        <DetailRow label="frame range" value={`${tracklet.frame_start} - ${tracklet.frame_end}`} />
        <DetailRow
          label="timestamp range"
          value={`${tracklet.timestamp_start_ms} - ${tracklet.timestamp_end_ms} ms`}
        />
        <DetailRow label="points" value={tracklet.points.length.toString()} />
        <a className="quiet-link" href={`/runs/${tracklet.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Tracklet candidate. Candidate temporal grouping only; it does not conclude identity or path
          correctness.
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "tracklet_timeline") {
    const { item } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Tracklet Candidate" badge={item.track_type}>
        <DetailRow label="tracklet id" value={item.tracklet_id} />
        <DetailRow label="observation id" value={item.observation_id ?? "n/a"} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="label hint" value={item.label_hint ?? "n/a"} />
        <DetailRow label="track_status" value={item.track_status} />
        <DetailRow label="identity_status" value={item.identity_status} />
        <DetailRow label="source detection run" value={item.source_detection_run_id ?? "n/a"} />
        <DetailRow label="source evidence" value={sourceDetectionDisplayLabel(item)} />
        <DetailRow label="source runtime" value={item.source_detection_runtime ?? "n/a"} />
        <DetailRow label="frame range" value={`${item.frame_start} - ${item.frame_end}`} />
        <DetailRow
          label="timestamp range"
          value={`${item.timestamp_start_ms} - ${item.timestamp_end_ms} ms`}
        />
        <DetailRow label="track points" value={item.track_point_count.toString()} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Tracklet candidate selected from the evidence timeline. Candidate temporal grouping only;
          it does not conclude identity or path correctness.
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "track_point") {
    const { tracklet, point } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Track Point Candidate" badge={tracklet.track_type}>
        <DetailRow label="track point id" value={point.track_point_id} />
        <DetailRow label="observation id" value={point.observation_id ?? "n/a"} />
        <DetailRow label="source detection" value={point.source_detection_observation_id ?? "n/a"} />
        <DetailRow label="source detection run" value={point.source_detection_run_id ?? "n/a"} />
        <DetailRow label="source evidence" value={sourceDetectionDisplayLabel(point)} />
        <DetailRow label="source runtime" value={point.source_detection_runtime ?? "n/a"} />
        <DetailRow label="tracklet id" value={tracklet.tracklet_id} />
        <DetailRow label="run id" value={tracklet.run_id} />
        <DetailRow label="frame" value={point.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={point.timestamp_ms.toString()} />
        <DetailRow label="center" value={`${point.x}, ${point.y}`} />
        <DetailRow label="confidence" value={formatConfidence(point.confidence)} />
        <a className="quiet-link" href={`/runs/${tracklet.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Track point candidate. Source-linked evidence only, without interpolation or smoothing.
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "pose_timeline") {
    const { item } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Pose Observation" badge="pose">
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="pose confidence" value={formatConfidence(item.pose_confidence)} />
        <DetailRow label="source" value={poseSourceDisplayLabel(item)} />
        <DetailRow label="source runtime" value={item.source_runtime ?? "n/a"} />
        <DetailRow
          label="model"
          value={formatModelNameVersion(item.model_name, item.model_version)}
        />
        <DetailRow label="model registry id" value={item.model_registry_id ?? "n/a"} />
        <DetailRow label="runtime config id" value={item.runtime_config_id ?? "n/a"} />
        <DetailRow
          label="keypoints"
          value={`${item.keypoints_present_count} present / ${item.keypoints_missing_count} missing`}
        />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Pose observation selected from the evidence timeline. Keypoint evidence only; it does not
          classify strokes, movement, or biomechanics.
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "annotation") {
    const { item } = selectedEvidence;
    return (
      <EvidencePanel title="Selected Review Annotation" badge={item.annotation_label}>
        <DetailRow label="annotation id" value={item.annotation_id} />
        <DetailRow label="target observation id" value={item.target_observation_id ?? "n/a"} />
        <DetailRow label="target observation type" value={item.target_observation_type ?? "n/a"} />
        <DetailRow label="target run id" value={item.target_run_id ?? "n/a"} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="created_by" value={item.created_by ?? "n/a"} />
        {item.target_run_id !== null ? (
          <a className="quiet-link" href={`/runs/${item.target_run_id}`}>
            Open target evidence run
          </a>
        ) : null}
        <p className="evidence-note">
          Review annotation. Annotations are non-mutating review evidence; they do not change model
          output or adjudicate tennis meaning.
        </p>
      </EvidencePanel>
    );
  }

  const { pose } = selectedEvidence;
  return (
    <EvidencePanel title="Selected Pose Observation" badge={pose.skeleton_format}>
      <DetailRow label="observation id" value={pose.observation_id} />
      <DetailRow label="run id" value={pose.run_id} />
      <DetailRow label="frame" value={pose.frame_number.toString()} />
      <DetailRow label="timestamp_ms" value={pose.timestamp_ms.toString()} />
      <DetailRow label="skeleton" value={`${pose.skeleton_format}/${pose.skeleton_version}`} />
      <DetailRow label="pose confidence" value={formatConfidence(pose.pose_confidence)} />
      <DetailRow label="source" value={poseSourceDisplayLabel(pose)} />
      <DetailRow label="source runtime" value={pose.source_runtime ?? "n/a"} />
      <DetailRow
        label="model"
        value={formatModelNameVersion(pose.model_name, pose.model_version)}
      />
      <DetailRow label="model registry id" value={pose.model_registry_id ?? "n/a"} />
      <DetailRow label="runtime config id" value={pose.runtime_config_id ?? "n/a"} />
      <DetailRow
        label="keypoints"
        value={`${pose.keypoints_present_count} present / ${pose.keypoints_missing_count} missing`}
      />
      <DetailRow
        label="subject context"
        value={`${pose.subject_context.subject_ref_type} · ${pose.subject_context.association_status}`}
      />
      <DetailRow label="association method" value={pose.subject_context.association_method ?? "n/a"} />
      <a className="quiet-link" href={`/runs/${pose.run_id}`}>
        Open source evidence run
      </a>
      <p className="evidence-note">
        Pose observation. Keypoint evidence only; it does not classify strokes, movement, or
        biomechanics.
      </p>
    </EvidencePanel>
  );
}

function EvidencePanel({
  title,
  badge,
  children
}: {
  title: string;
  badge: string;
  children: ReactNode;
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>{title}</h2>
        <span className="mini-pill">{badge}</span>
      </div>
      <div className="panel-body replay-media-detail">{children}</div>
    </section>
  );
}

function RunGroup({ title, runs }: { title: string; runs: ReplayRunSummary[] }) {
  return (
    <div className="run-group">
      <h3>{title}</h3>
      {runs.length === 0 ? (
        <p className="empty-state compact">
          No {title.toLowerCase()} are attached to this media yet.
        </p>
      ) : (
        <ul>
          {runs.map((run) => (
            <li key={run.run_id}>
              <strong>{run.run_name}</strong>
              <span className="mono">{run.run_id}</span>
              <span>
                {run.run_status} · {run.observation_count} observations ·{" "}
                {formatReplayRunSourceLabel(run)}
              </span>
              {run.model_registry_id !== null && run.model_registry_id !== undefined ? (
                <span className="mono">
                  {formatModelNameVersion(run.model_name, run.model_version)} ·{" "}
                  {run.source_runtime ?? "unknown runtime"}
                </span>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function SelectedRunRow({
  label,
  runId,
  runs
}: {
  label: string;
  runId?: string;
  runs: ReplayRunSummary[];
}) {
  const run = runs.find((candidate) => candidate.run_id === runId);
  return (
    <div className="selected-run-row">
      <strong>{label}</strong>
      {runId === undefined ? (
        <span className="empty-state compact">No run selected.</span>
      ) : run === undefined ? (
        <span className="empty-state compact">Selected run is not available for this media.</span>
      ) : (
        <span>
          {run.run_name} · {run.observation_count} observations ·{" "}
          {formatReplayRunSourceLabel(run)}
        </span>
      )}
    </div>
  );
}

function selectedTimelineItemKey(selectedEvidence: SelectedReplayEvidence | null): string | null {
  if (selectedEvidence === null) {
    return null;
  }
  if (selectedEvidence.kind === "detection") {
    return `detection:${selectedEvidence.detection.observation_id}`;
  }
  if (selectedEvidence.kind === "tracklet") {
    return `tracklet:${selectedEvidence.tracklet.tracklet_id}`;
  }
  if (selectedEvidence.kind === "track_point") {
    return `tracklet:${selectedEvidence.tracklet.tracklet_id}`;
  }
  if (selectedEvidence.kind === "pose") {
    return `pose:${selectedEvidence.pose.observation_id}`;
  }
  return timelineItemKey(selectedEvidence.item);
}

function formatReplayRunOptionLabel(run: ReplayRunSummary): string {
  return `${run.run_name} — ${formatReplayRunSourceLabel(run)} — ${run.observation_count} observations`;
}

function formatReplayRunSourceLabel(run: ReplayRunSummary): string {
  if (run.evidence_source === "real_pose_model_output") {
    return "real pose model output";
  }
  if (run.is_real_model_output || run.evidence_source === "real_model_output") {
    return "real model output";
  }
  if (
    run.is_real_detection_derived ||
    run.evidence_source === "real_detection_derived_tracklet"
  ) {
    return "real-detection-derived tracklet candidates";
  }
  if (run.evidence_source === "fixture_derived_tracklet") {
    return "fixture-derived tracklet candidates";
  }
  if (run.is_fixture || run.evidence_source === "fixture_demo") {
    return "fixture demo evidence";
  }
  return run.source_label ?? "persisted evidence";
}

function sourceDisplayLabel(
  item:
    | ReplayDetectionOverlay
    | Extract<ReplayTimelineItem, { item_type: "detection" }>
): string {
  if (item.real_model_output || item.evidence_source === "real_model_output") {
    return "Real model output";
  }
  if (item.is_fixture || item.evidence_source === "fixture_demo") {
    return "Fixture/demo evidence";
  }
  return item.source_label ?? "Persisted evidence";
}

function poseSourceDisplayLabel(
  item: ReplayPoseOverlay | Extract<ReplayTimelineItem, { item_type: "pose" }>
): string {
  if (item.evidence_source === "real_pose_model_output" || item.real_model_output) {
    return "Real pose model output";
  }
  if (item.is_fixture || item.evidence_source === "fixture_demo") {
    return "Fixture/demo evidence";
  }
  return item.source_label ?? "Persisted pose evidence";
}

function sourceDetectionDisplayLabel(
  item:
    | ReplayTrackletOverlay
    | ReplayTrackPointOverlay
    | Extract<ReplayTimelineItem, { item_type: "tracklet" }>
): string {
  if (
    item.source_detection_real_model_output ||
    item.source_detection_evidence_source === "real_model_output"
  ) {
    return "Real model output";
  }
  if (item.source_detection_evidence_source === "fixture_demo") {
    return "Fixture/demo evidence";
  }
  return item.source_detection_source_label ?? "Persisted detection evidence";
}

function formatModelNameVersion(
  modelName: string | null | undefined,
  modelVersion: string | null | undefined
): string {
  if (!modelName && !modelVersion) {
    return "n/a";
  }
  if (!modelVersion) {
    return modelName ?? "n/a";
  }
  if (!modelName) {
    return modelVersion;
  }
  return `${modelName} / ${modelVersion}`;
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="detail-row">
      <strong>{label}</strong>
      <span className="mono">{value}</span>
    </div>
  );
}

function TelemetryLikeCell({ label, value }: { label: string; value: string }) {
  return (
    <div className="media-cell">
      <strong>{label}</strong>
      <span>{value}</span>
    </div>
  );
}
