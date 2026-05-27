"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { fetchReplayOverlayChunk } from "../lib/api";
import {
  selectInitialDetectionRun
} from "../lib/replayOverlays";
import type {
  ReplayDetectionOverlay,
  ReplayInfo,
  ReplayOverlayChunk,
  ReplayPlaybackState,
  ReplayRunSummary
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";
import { ReplayDetectionOverlay as ReplayDetectionOverlayLayer } from "./ReplayDetectionOverlay";
import { ReplayVideoPlayer } from "./ReplayVideoPlayer";

const overlayChunkMs = 2000;

interface ReplayWorkstationProps {
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

export function ReplayWorkstation({ replayInfo, selectedRuns }: ReplayWorkstationProps) {
  const initialDetectionRunId = useMemo(
    () => selectInitialDetectionRun(replayInfo.available_runs.detection, selectedRuns.detectionRunId),
    [replayInfo.available_runs.detection, selectedRuns.detectionRunId]
  );
  const [selectedDetectionRunId, setSelectedDetectionRunId] = useState<string | null>(
    initialDetectionRunId
  );
  const [showDetections, setShowDetections] = useState(true);
  const [selectedDetection, setSelectedDetection] = useState<ReplayDetectionOverlay | null>(null);
  const [playback, setPlayback] = useState<ReplayPlaybackState>({
    currentTimeSeconds: 0,
    timestampMs: 0,
    frameNumber: 0,
    durationSeconds: replayInfo.duration_ms !== null ? replayInfo.duration_ms / 1000 : 0
  });
  const [overlayState, setOverlayState] = useState<OverlayState>({
    chunk: null,
    loading: false,
    error: null
  });
  const chunkCache = useRef<Map<string, ReplayOverlayChunk>>(new Map());

  useEffect(() => {
    setSelectedDetectionRunId(initialDetectionRunId);
  }, [initialDetectionRunId]);

  const currentChunkStart = Math.floor(playback.timestampMs / overlayChunkMs) * overlayChunkMs;
  const currentChunkEnd = currentChunkStart + overlayChunkMs;
  const chunkKey = [
    replayInfo.media_id,
    selectedDetectionRunId ?? "all",
    currentChunkStart,
    currentChunkEnd
  ].join(":");

  useEffect(() => {
    if (!showDetections || selectedDetectionRunId === null) {
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
      layers: "detections"
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
            error: error instanceof Error ? error.message : "Unable to load detection overlays"
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
    replayInfo.media_id,
    selectedDetectionRunId,
    showDetections
  ]);

  const handlePlaybackStateChange = useCallback((state: ReplayPlaybackState) => {
    setPlayback(state);
  }, []);

  const detections = overlayState.chunk?.detections ?? [];

  return (
    <main className="viewer-shell replay-shell">
      <header className="viewer-header">
        <div className="viewer-title">
          <p className="eyebrow">TOM v3 Replay Workstation</p>
          <h1>Detection overlay playback</h1>
          <div className="meta-line">
            <span className="status-pill">observation-only</span>
            <span className="mini-pill">no adjudication</span>
            <span className="mono">{replayInfo.media_id}</span>
          </div>
        </div>
        <div className="meta-line">
          <span className="mini-pill">{replayInfo.frame_time_mode} frame/time</span>
          <span className="mini-pill">{replayInfo.available_runs.detection.length} detection runs</span>
          <span className="mini-pill">{detections.length} loaded detection overlays</span>
        </div>
      </header>

      <div className="replay-grid">
        <div className="main-column">
          <ReplayVideoPlayer
            onPlaybackStateChange={handlePlaybackStateChange}
            replayInfo={replayInfo}
          >
            <ReplayDetectionOverlayLayer
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              detections={detections}
              enabled={showDetections && selectedDetectionRunId !== null}
              error={overlayState.error}
              isLoading={overlayState.loading}
              onSelectObservation={setSelectedDetection}
              replayInfo={replayInfo}
              selectedObservationId={selectedDetection?.observation_id ?? null}
            />
          </ReplayVideoPlayer>
          <DetectionControls
            detectionRuns={replayInfo.available_runs.detection}
            onSelectedRunChange={(runId) => {
              setSelectedDetectionRunId(runId);
              setSelectedDetection(null);
            }}
            onToggleLayer={setShowDetections}
            selectedDetectionRunId={selectedDetectionRunId}
            showDetections={showDetections}
          />
          <DetectionTimelineTicks
            detections={detections}
            onSelectDetection={setSelectedDetection}
            selectedObservationId={selectedDetection?.observation_id ?? null}
          />
          <SelectedRunContext
            replayInfo={replayInfo}
            selectedDetectionRunId={selectedDetectionRunId}
            selectedRuns={selectedRuns}
          />
        </div>
        <aside className="side-column">
          <ReplayMediaPanel replayInfo={replayInfo} />
          <SelectedDetectionPanel detection={selectedDetection} />
          <AvailableRunsPanel replayInfo={replayInfo} />
          <section className="panel">
            <div className="panel-header">
              <h2>Future Overlay Layers</h2>
              <span className="mini-pill">deferred</span>
            </div>
            <div className="panel-body">
              <p className="empty-state">
                Tracklet candidate and pose observation playback overlays come later. This milestone
                renders persisted detection observations only.
              </p>
            </div>
          </section>
        </aside>
      </div>
    </main>
  );
}

function DetectionControls({
  detectionRuns,
  selectedDetectionRunId,
  showDetections,
  onSelectedRunChange,
  onToggleLayer
}: {
  detectionRuns: ReplayRunSummary[];
  selectedDetectionRunId: string | null;
  showDetections: boolean;
  onSelectedRunChange: (runId: string | null) => void;
  onToggleLayer: (enabled: boolean) => void;
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Detection Layer</h2>
        <span className="mini-pill">persisted bbox evidence</span>
      </div>
      <div className="panel-body replay-controls">
        <label className="toggle-row">
          <input
            checked={showDetections}
            onChange={(event) => onToggleLayer(event.target.checked)}
            type="checkbox"
          />
          <span>Show detection observations</span>
        </label>
        <label className="select-row">
          <span>Detection run</span>
          <select
            onChange={(event) => onSelectedRunChange(event.target.value || null)}
            value={selectedDetectionRunId ?? ""}
          >
            <option value="">Select a detection run</option>
            {detectionRuns.map((run) => (
              <option key={run.run_id} value={run.run_id}>
                {run.run_name} ({run.observation_count})
              </option>
            ))}
          </select>
        </label>
        <p className="evidence-note">
          Bboxes are persisted detection observations. The display hold is visual only and does not
          alter evidence.
        </p>
      </div>
    </section>
  );
}

function DetectionTimelineTicks({
  detections,
  selectedObservationId,
  onSelectDetection
}: {
  detections: ReplayDetectionOverlay[];
  selectedObservationId: string | null;
  onSelectDetection: (detection: ReplayDetectionOverlay) => void;
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Detection Timeline Ticks</h2>
        <span className="mini-pill">{detections.length} in loaded chunk</span>
      </div>
      <div className="panel-body detection-tick-list">
        {detections.length === 0 ? (
          <p className="empty-state">
            No detection observations loaded for this replay window yet.
          </p>
        ) : (
          detections.map((detection) => (
            <button
              className={`detection-tick-row${
                detection.observation_id === selectedObservationId ? " selected" : ""
              }`}
              key={detection.observation_id}
              onClick={() => onSelectDetection(detection)}
              type="button"
            >
              <strong>{detection.label}</strong>
              <span>frame {detection.frame_number}</span>
              <span>{detection.timestamp_ms} ms</span>
              <span>{formatConfidence(detection.confidence)}</span>
            </button>
          ))
        )}
      </div>
    </section>
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
  selectedRuns,
  selectedDetectionRunId
}: {
  replayInfo: ReplayInfo;
  selectedRuns: {
    detectionRunId?: string;
    trackletRunId?: string;
    poseRunId?: string;
  };
  selectedDetectionRunId: string | null;
}) {
  const selected = [
    ["detection", selectedDetectionRunId ?? selectedRuns.detectionRunId, replayInfo.available_runs.detection],
    ["tracklet candidate", selectedRuns.trackletRunId, replayInfo.available_runs.tracklet],
    ["pose observation", selectedRuns.poseRunId, replayInfo.available_runs.pose]
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
          Detection context drives 6B overlay playback. Tracklet and pose context are displayed
          only; their overlays come later.
        </p>
      </div>
    </section>
  );
}

function SelectedDetectionPanel({ detection }: { detection: ReplayDetectionOverlay | null }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Selected Detection Observation</h2>
        <span className="mini-pill">{detection === null ? "none" : detection.observation_type}</span>
      </div>
      <div className="panel-body replay-media-detail">
        {detection === null ? (
          <p className="empty-state">
            Click a replay bbox to inspect persisted detection observation details.
          </p>
        ) : (
          <>
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
            <a className="quiet-link" href={`/runs/${detection.run_id}`}>
              Open source evidence run
            </a>
            <p className="evidence-note">
              Detection observation. Evidence only, not a confirmed object or tennis event.
            </p>
          </>
        )}
      </div>
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
                {run.run_status} · {run.observation_count} observations
              </span>
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
          {run.run_name} · {run.observation_count} observations
        </span>
      )}
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="detail-row">
      <strong>{label}</strong>
      <span className="mono">{value}</span>
    </div>
  );
}
