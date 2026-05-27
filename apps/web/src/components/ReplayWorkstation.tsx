"use client";

import type { ReactNode } from "react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { fetchReplayOverlayChunk } from "../lib/api";
import { selectInitialReplayRun } from "../lib/replayOverlays";
import type {
  ReplayDetectionOverlay,
  ReplayInfo,
  ReplayOverlayChunk,
  ReplayPlaybackState,
  ReplayPoseOverlay,
  ReplayRunSummary,
  ReplayTrackletOverlay,
  ReplayTrackPointOverlay
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";
import { ReplayDetectionOverlay as ReplayDetectionOverlayLayer } from "./ReplayDetectionOverlay";
import { ReplayPoseOverlay as ReplayPoseOverlayLayer } from "./ReplayPoseOverlay";
import { ReplayTrackletOverlay as ReplayTrackletOverlayLayer } from "./ReplayTrackletOverlay";
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

type SelectedReplayEvidence =
  | { kind: "detection"; detection: ReplayDetectionOverlay }
  | { kind: "tracklet"; tracklet: ReplayTrackletOverlay }
  | { kind: "track_point"; tracklet: ReplayTrackletOverlay; point: ReplayTrackPointOverlay }
  | { kind: "pose"; pose: ReplayPoseOverlay };

export function ReplayWorkstation({ replayInfo, selectedRuns }: ReplayWorkstationProps) {
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
  const [selectedEvidence, setSelectedEvidence] = useState<SelectedReplayEvidence | null>(null);
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

  useEffect(() => {
    setSelectedTrackletRunId(initialTrackletRunId);
  }, [initialTrackletRunId]);

  useEffect(() => {
    setSelectedPoseRunId(initialPoseRunId);
  }, [initialPoseRunId]);

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

  const handlePlaybackStateChange = useCallback((state: ReplayPlaybackState) => {
    setPlayback(state);
  }, []);

  const detections = overlayState.chunk?.detections ?? [];
  const tracklets = overlayState.chunk?.tracklets ?? [];
  const poses = overlayState.chunk?.poses ?? [];
  const selectedDetectionId =
    selectedEvidence?.kind === "detection" ? selectedEvidence.detection.observation_id : null;
  const selectedTrackletId =
    selectedEvidence?.kind === "tracklet"
      ? selectedEvidence.tracklet.tracklet_id
      : selectedEvidence?.kind === "track_point"
        ? selectedEvidence.tracklet.tracklet_id
        : null;
  const selectedTrackPointId =
    selectedEvidence?.kind === "track_point" ? selectedEvidence.point.track_point_id : null;
  const selectedPoseObservationId =
    selectedEvidence?.kind === "pose" ? selectedEvidence.pose.observation_id : null;

  return (
    <main className="viewer-shell replay-shell">
      <header className="viewer-header">
        <div className="viewer-title">
          <p className="eyebrow">TOM v3 Replay Workstation</p>
          <h1>Tracklet and pose overlay playback</h1>
          <div className="meta-line">
            <span className="status-pill">observation-only</span>
            <span className="mini-pill">no adjudication</span>
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
            replayInfo={replayInfo}
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
          <OverlayTimelineTicks
            detections={detections}
            onSelectDetection={(detection) => setSelectedEvidence({ kind: "detection", detection })}
            onSelectPose={(pose) => setSelectedEvidence({ kind: "pose", pose })}
            onSelectTracklet={(tracklet) => setSelectedEvidence({ kind: "tracklet", tracklet })}
            poses={poses}
            selectedEvidence={selectedEvidence}
            tracklets={tracklets}
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
          <section className="panel">
            <div className="panel-header">
              <h2>Future Timeline Lanes</h2>
              <span className="mini-pill">6D</span>
            </div>
            <div className="panel-body">
              <p className="empty-state">
                Detection, tracklet candidate, and pose observation overlays now play over video.
                Full evidence lanes and richer scrubbing arrive in the next replay milestone.
              </p>
            </div>
          </section>
        </aside>
      </div>
    </main>
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
            {run.run_name} ({run.observation_count})
          </option>
        ))}
      </select>
    </label>
  );
}

function OverlayTimelineTicks({
  detections,
  tracklets,
  poses,
  selectedEvidence,
  onSelectDetection,
  onSelectTracklet,
  onSelectPose
}: {
  detections: ReplayDetectionOverlay[];
  tracklets: ReplayTrackletOverlay[];
  poses: ReplayPoseOverlay[];
  selectedEvidence: SelectedReplayEvidence | null;
  onSelectDetection: (detection: ReplayDetectionOverlay) => void;
  onSelectTracklet: (tracklet: ReplayTrackletOverlay) => void;
  onSelectPose: (pose: ReplayPoseOverlay) => void;
}) {
  const itemCount = detections.length + tracklets.length + poses.length;
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Loaded Overlay Ticks</h2>
        <span className="mini-pill">{itemCount} loaded items</span>
      </div>
      <div className="panel-body detection-tick-list">
        {itemCount === 0 ? (
          <p className="empty-state">
            No replay overlays loaded for this window. Select runs and play or scrub the video.
          </p>
        ) : (
          <>
            {detections.map((detection) => (
              <button
                className={`detection-tick-row${
                  selectedEvidence?.kind === "detection" &&
                  selectedEvidence.detection.observation_id === detection.observation_id
                    ? " selected"
                    : ""
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
            ))}
            {tracklets.map((tracklet) => (
              <button
                className={`detection-tick-row${
                  selectedEvidence?.kind === "tracklet" &&
                  selectedEvidence.tracklet.tracklet_id === tracklet.tracklet_id
                    ? " selected"
                    : ""
                }`}
                key={tracklet.tracklet_id}
                onClick={() => onSelectTracklet(tracklet)}
                type="button"
              >
                <strong>{tracklet.label_hint ?? tracklet.track_type}</strong>
                <span>candidate path</span>
                <span>
                  {tracklet.timestamp_start_ms}-{tracklet.timestamp_end_ms} ms
                </span>
                <span>{tracklet.points.length} points</span>
              </button>
            ))}
            {poses.map((pose) => (
              <button
                className={`detection-tick-row${
                  selectedEvidence?.kind === "pose" &&
                  selectedEvidence.pose.observation_id === pose.observation_id
                    ? " selected"
                    : ""
                }`}
                key={pose.observation_id}
                onClick={() => onSelectPose(pose)}
                type="button"
              >
                <strong>pose evidence</strong>
                <span>frame {pose.frame_number}</span>
                <span>{pose.timestamp_ms} ms</span>
                <span>{pose.keypoints_present_count} present</span>
              </button>
            ))}
          </>
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
        <a className="quiet-link" href={`/runs/${detection.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Detection observation. Evidence only, not a confirmed object or tennis event.
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
          Tracklet candidate. Candidate temporal grouping only; it does not confirm identity or path
          correctness.
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

  const { pose } = selectedEvidence;
  return (
    <EvidencePanel title="Selected Pose Observation" badge={pose.skeleton_format}>
      <DetailRow label="observation id" value={pose.observation_id} />
      <DetailRow label="run id" value={pose.run_id} />
      <DetailRow label="frame" value={pose.frame_number.toString()} />
      <DetailRow label="timestamp_ms" value={pose.timestamp_ms.toString()} />
      <DetailRow label="skeleton" value={`${pose.skeleton_format}/${pose.skeleton_version}`} />
      <DetailRow label="pose confidence" value={formatConfidence(pose.pose_confidence)} />
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
