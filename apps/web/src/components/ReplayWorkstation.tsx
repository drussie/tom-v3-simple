"use client";

import type { ReactNode } from "react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { fetchReplayOverlayChunk, fetchReplayTimeline } from "../lib/api";
import {
  filterCameraViewsAvailableAt,
  filterCourtKeypointsAvailableAt,
  filterCourtLinesAvailableAt,
  filterEventCandidatesAvailableAt,
  filterBallCourtTrajectoryAvailableAt,
  filterBallCourtProjectionAvailableAt,
  filterDetectionsAvailableAt,
  filterHomographyCandidatesAvailableAt,
  filterMainPlayerCourtProjectionAvailableAt,
  filterMainPlayerTracksAvailableAt,
  filterPosesAvailableAt,
  filterProjectionDiagnosticsAvailableAt,
  filterSmoothedBallAvailableAt,
  filterSmoothedPlayerBoxesAvailableAt,
  filterSmoothedPosesAvailableAt,
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
  ReplayBallCourtTrajectoryOverlay,
  ReplayDetectionOverlay,
  ReplayBallCourtProjectionOverlay,
  ReplayCameraViewOverlay,
  ReplayCourtEvidenceSource,
  ReplayCourtTemporalPersistence,
  ReplayCourtKeypointOverlay,
  ReplayCourtLineOverlay,
  ReplayEventCandidateOverlay,
  ReplayHomographyCandidateOverlay,
  ReplayMainPlayerCourtProjectionOverlay,
  ReplayInfo,
  ReplayLayerPreset,
  ReplayMainPlayerTrackOverlay,
  ReplayMode,
  ReplayOverlayDisplayMode,
  ReplayOverlayChunk,
  ReplayPlaybackState,
  ReplayPoseOverlay,
  ReplayPoseVisualStyle,
  ReplayProjectionDiagnosticOverlay,
  ReplayRunSummary,
  ReplaySeekRequest,
  ReplaySmoothedBallOverlay,
  ReplaySmoothedMotionTimelineItem,
  ReplaySmoothedPlayerBoxOverlay,
  ReplaySmoothedPoseOverlay,
  ReplayTimeline,
  ReplayTimelineItem,
  ReplayTrackletOverlay,
  ReplayTrackPointOverlay
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";
import { ReplayCourtOverlay as ReplayCourtOverlayLayer } from "./ReplayCourtOverlay";
import { ReplayCourtProjectionMiniMap } from "./ReplayCourtProjectionMiniMap";
import { ReplayDetectionOverlay as ReplayDetectionOverlayLayer } from "./ReplayDetectionOverlay";
import { ReplayEventCandidateVideoOverlay } from "./ReplayEventCandidateVideoOverlay";
import { ReplayEvidenceTimeline } from "./ReplayEvidenceTimeline";
import { ReplayMainPlayerTrackOverlay as ReplayMainPlayerTrackOverlayLayer } from "./ReplayMainPlayerTrackOverlay";
import { ReplayPoseOverlay as ReplayPoseOverlayLayer } from "./ReplayPoseOverlay";
import { ReplaySmoothedMotionOverlay as ReplaySmoothedMotionOverlayLayer } from "./ReplaySmoothedMotionOverlay";
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
    mainPlayerTrackRunId?: string;
    motionSmoothingRunId?: string;
    courtRunId?: string;
    courtTemporalPersistence?: string;
    courtPersistenceMaxGapMs?: string;
    homographyRunId?: string;
    projectionDiagnosticRunId?: string;
    courtProjectionRunId?: string;
    ballTrajectoryRunId?: string;
    eventCandidateRunId?: string;
    viewPreset?: string;
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
  | { kind: "main_player_track"; item: ReplayMainPlayerTrackOverlay }
  | { kind: "main_player_track_timeline"; item: Extract<ReplayTimelineItem, { item_type: "main_player_track_assignment" }> }
  | { kind: "smoothed_ball"; item: ReplaySmoothedBallOverlay }
  | { kind: "smoothed_player_box"; item: ReplaySmoothedPlayerBoxOverlay }
  | { kind: "smoothed_pose"; item: ReplaySmoothedPoseOverlay }
  | { kind: "smoothed_motion_timeline"; item: ReplaySmoothedMotionTimelineItem }
  | { kind: "court_keypoint"; item: ReplayCourtKeypointOverlay }
  | { kind: "court_keypoint_timeline"; item: Extract<ReplayTimelineItem, { item_type: "court_keypoint" }> }
  | { kind: "court_line"; item: ReplayCourtLineOverlay }
  | { kind: "court_line_timeline"; item: Extract<ReplayTimelineItem, { item_type: "court_line" }> }
  | { kind: "camera_view"; item: ReplayCameraViewOverlay }
  | { kind: "camera_view_timeline"; item: Extract<ReplayTimelineItem, { item_type: "camera_view" }> }
  | { kind: "homography_candidate"; item: ReplayHomographyCandidateOverlay }
  | { kind: "homography_candidate_timeline"; item: Extract<ReplayTimelineItem, { item_type: "homography_candidate" }> }
  | { kind: "projection_diagnostic"; item: ReplayProjectionDiagnosticOverlay }
  | { kind: "projection_diagnostic_timeline"; item: Extract<ReplayTimelineItem, { item_type: "projection_diagnostic" }> }
  | { kind: "ball_court_projection"; item: ReplayBallCourtProjectionOverlay }
  | { kind: "main_player_court_projection"; item: ReplayMainPlayerCourtProjectionOverlay }
  | { kind: "court_projection_timeline"; item: Extract<ReplayTimelineItem, { item_type: "ball_court_projection_candidate" | "main_player_court_projection_candidate" }> }
  | { kind: "ball_trajectory"; item: ReplayBallCourtTrajectoryOverlay }
  | { kind: "ball_trajectory_timeline"; item: Extract<ReplayTimelineItem, { item_type: "ball_trajectory_court_candidate" }> }
  | { kind: "event_candidate"; item: ReplayEventCandidateOverlay }
  | { kind: "event_candidate_timeline"; item: Extract<ReplayTimelineItem, { item_type: "hit_candidate" | "bounce_candidate" }> }
  | { kind: "annotation"; item: Extract<ReplayTimelineItem, { item_type: "annotation" }> };

interface ReplayLayerPresetContext {
  hasDetectionRun: boolean;
  hasTrackletRun: boolean;
  hasPoseRun: boolean;
  hasMainPlayerTrackRun: boolean;
  hasMotionSmoothingRun: boolean;
  hasCourtRun: boolean;
  hasHomographyRun: boolean;
  hasProjectionDiagnosticRun: boolean;
  hasCourtProjectionRun: boolean;
  hasBallTrajectoryRun: boolean;
  hasEventCandidateRun: boolean;
}

interface ReplayLayerPresetVisibility {
  showDetections: boolean;
  showTracklets: boolean;
  showTrackletPaths: boolean;
  showPoses: boolean;
  showMainPlayerTracks: boolean;
  showSmoothedBall: boolean;
  showSmoothedPlayerBoxes: boolean;
  showSmoothedPoses: boolean;
  showRawCourtKeypoints: boolean;
  showCourtKeypoints: boolean;
  showCourtLines: boolean;
  showCameraView: boolean;
  showHomography: boolean;
  showProjectionDiagnostics: boolean;
  showBallCourtProjection: boolean;
  showMainPlayerCourtProjection: boolean;
  showBallCourtTrajectory: boolean;
  showEventCandidates: boolean;
  detectionDisplayMode: ReplayOverlayDisplayMode;
  trackletDisplayMode: ReplayOverlayDisplayMode;
  smoothedMotionDisplayMode: ReplayOverlayDisplayMode;
  poseVisualStyle: ReplayPoseVisualStyle;
  courtTemporalPersistence: ReplayCourtTemporalPersistence;
}

export function normalizeReplayLayerPreset(value: string | undefined): ReplayLayerPreset {
  return value === "debug" ? "debug" : "operator";
}

export function applyLayerPreset(
  preset: ReplayLayerPreset,
  context: ReplayLayerPresetContext
): ReplayLayerPresetVisibility {
  if (preset === "debug") {
    return {
      showDetections: context.hasDetectionRun,
      showTracklets: context.hasTrackletRun,
      showTrackletPaths: context.hasTrackletRun,
      showPoses: context.hasPoseRun,
      showMainPlayerTracks: context.hasMainPlayerTrackRun,
      showSmoothedBall: context.hasMotionSmoothingRun,
      showSmoothedPlayerBoxes: context.hasMotionSmoothingRun,
      showSmoothedPoses: context.hasMotionSmoothingRun,
      showRawCourtKeypoints: context.hasCourtRun,
      showCourtKeypoints: context.hasCourtRun,
      showCourtLines: context.hasCourtRun,
      showCameraView: context.hasCourtRun,
      showHomography: context.hasHomographyRun,
      showProjectionDiagnostics: context.hasProjectionDiagnosticRun,
      showBallCourtProjection: context.hasCourtProjectionRun,
      showMainPlayerCourtProjection: context.hasCourtProjectionRun,
      showBallCourtTrajectory: context.hasBallTrajectoryRun,
      showEventCandidates: context.hasEventCandidateRun,
      detectionDisplayMode: "short_trail",
      trackletDisplayMode: "full_trail",
      smoothedMotionDisplayMode: "short_trail",
      poseVisualStyle: "limbs_and_joints",
      courtTemporalPersistence: "carry_forward"
    };
  }

  return {
    showDetections: context.hasDetectionRun && !context.hasMotionSmoothingRun,
    showTracklets: context.hasTrackletRun && !context.hasMotionSmoothingRun,
    showTrackletPaths: false,
    showPoses: context.hasPoseRun && !context.hasMotionSmoothingRun,
    showMainPlayerTracks: context.hasMainPlayerTrackRun && !context.hasMotionSmoothingRun,
    showSmoothedBall: context.hasMotionSmoothingRun,
    showSmoothedPlayerBoxes: context.hasMotionSmoothingRun,
    showSmoothedPoses: context.hasMotionSmoothingRun,
    showRawCourtKeypoints: false,
    showCourtKeypoints: context.hasCourtRun,
    showCourtLines: context.hasCourtRun,
    showCameraView: false,
    showHomography: false,
    showProjectionDiagnostics: false,
    showBallCourtProjection: context.hasCourtProjectionRun,
    showMainPlayerCourtProjection: context.hasCourtProjectionRun,
    showBallCourtTrajectory: context.hasBallTrajectoryRun,
    showEventCandidates: context.hasEventCandidateRun,
    detectionDisplayMode: "current_only",
    trackletDisplayMode: "short_trail",
    smoothedMotionDisplayMode: "current_only",
    poseVisualStyle: "limbs_only",
    courtTemporalPersistence: "carry_forward"
  };
}

function presetContextFromRunIds({
  detectionRunId,
  trackletRunId,
  poseRunId,
  mainPlayerTrackRunId,
  motionSmoothingRunId,
  courtRunId,
  homographyRunId,
  projectionDiagnosticRunId,
  courtProjectionRunId,
  ballTrajectoryRunId,
  eventCandidateRunId
}: {
  detectionRunId: string | null;
  trackletRunId: string | null;
  poseRunId: string | null;
  mainPlayerTrackRunId: string | null;
  motionSmoothingRunId: string | null;
  courtRunId: string | null;
  homographyRunId: string | null;
  projectionDiagnosticRunId: string | null;
  courtProjectionRunId: string | null;
  ballTrajectoryRunId: string | null;
  eventCandidateRunId: string | null;
}): ReplayLayerPresetContext {
  return {
    hasDetectionRun: detectionRunId !== null,
    hasTrackletRun: trackletRunId !== null,
    hasPoseRun: poseRunId !== null,
    hasMainPlayerTrackRun: mainPlayerTrackRunId !== null,
    hasMotionSmoothingRun: motionSmoothingRunId !== null,
    hasCourtRun: courtRunId !== null,
    hasHomographyRun: homographyRunId !== null,
    hasProjectionDiagnosticRun: projectionDiagnosticRunId !== null,
    hasCourtProjectionRun: courtProjectionRunId !== null,
    hasBallTrajectoryRun: ballTrajectoryRunId !== null,
    hasEventCandidateRun: eventCandidateRunId !== null
  };
}

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
  const initialMainPlayerTrackRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.main_player_track,
        selectedRuns.mainPlayerTrackRunId
      ),
    [replayInfo.available_runs.main_player_track, selectedRuns.mainPlayerTrackRunId]
  );
  const initialMotionSmoothingRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.motion_smoothing,
        selectedRuns.motionSmoothingRunId
      ),
    [replayInfo.available_runs.motion_smoothing, selectedRuns.motionSmoothingRunId]
  );
  const initialCourtRunId = useMemo(
    () => selectInitialReplayRun(replayInfo.available_runs.court, selectedRuns.courtRunId),
    [replayInfo.available_runs.court, selectedRuns.courtRunId]
  );
  const initialHomographyRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.homography,
        selectedRuns.homographyRunId
      ),
    [replayInfo.available_runs.homography, selectedRuns.homographyRunId]
  );
  const initialProjectionDiagnosticRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.projection_diagnostic,
        selectedRuns.projectionDiagnosticRunId
      ),
    [
      replayInfo.available_runs.projection_diagnostic,
      selectedRuns.projectionDiagnosticRunId
    ]
  );
  const initialCourtProjectionRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.court_projection,
        selectedRuns.courtProjectionRunId
      ),
    [replayInfo.available_runs.court_projection, selectedRuns.courtProjectionRunId]
  );
  const initialBallTrajectoryRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.ball_trajectory,
        selectedRuns.ballTrajectoryRunId
      ),
    [replayInfo.available_runs.ball_trajectory, selectedRuns.ballTrajectoryRunId]
  );
  const initialEventCandidateRunId = useMemo(
    () =>
      selectInitialReplayRun(
        replayInfo.available_runs.event_candidate,
        selectedRuns.eventCandidateRunId
      ),
    [replayInfo.available_runs.event_candidate, selectedRuns.eventCandidateRunId]
  );
  const initialCourtTemporalPersistence = useMemo<ReplayCourtTemporalPersistence>(() => {
    return selectedRuns.courtTemporalPersistence === "off" ? "off" : "carry_forward";
  }, [selectedRuns.courtTemporalPersistence]);
  const initialCourtPersistenceMaxGapMs = useMemo(() => {
    const parsed = Number.parseInt(selectedRuns.courtPersistenceMaxGapMs ?? "", 10);
    return Number.isFinite(parsed) && parsed >= 0 ? parsed : 1500;
  }, [selectedRuns.courtPersistenceMaxGapMs]);
  const initialReplayLayerPreset = useMemo(
    () => normalizeReplayLayerPreset(selectedRuns.viewPreset),
    [selectedRuns.viewPreset]
  );
  const initialLayerPresetContext = useMemo(
    () =>
      presetContextFromRunIds({
        detectionRunId: initialDetectionRunId,
        trackletRunId: initialTrackletRunId,
        poseRunId: initialPoseRunId,
        mainPlayerTrackRunId: initialMainPlayerTrackRunId,
        motionSmoothingRunId: initialMotionSmoothingRunId,
        courtRunId: initialCourtRunId,
        homographyRunId: initialHomographyRunId,
        projectionDiagnosticRunId: initialProjectionDiagnosticRunId,
        courtProjectionRunId: initialCourtProjectionRunId,
        ballTrajectoryRunId: initialBallTrajectoryRunId,
        eventCandidateRunId: initialEventCandidateRunId
      }),
    [
      initialBallTrajectoryRunId,
      initialCourtProjectionRunId,
      initialCourtRunId,
      initialDetectionRunId,
      initialHomographyRunId,
      initialMainPlayerTrackRunId,
      initialMotionSmoothingRunId,
      initialPoseRunId,
      initialProjectionDiagnosticRunId,
      initialTrackletRunId,
      initialEventCandidateRunId
    ]
  );
  const initialLayerPresetState = useMemo(
    () => applyLayerPreset(initialReplayLayerPreset, initialLayerPresetContext),
    [initialLayerPresetContext, initialReplayLayerPreset]
  );

  const [selectedDetectionRunId, setSelectedDetectionRunId] = useState<string | null>(
    initialDetectionRunId
  );
  const [selectedTrackletRunId, setSelectedTrackletRunId] = useState<string | null>(
    initialTrackletRunId
  );
  const [selectedPoseRunId, setSelectedPoseRunId] = useState<string | null>(initialPoseRunId);
  const [selectedMainPlayerTrackRunId, setSelectedMainPlayerTrackRunId] = useState<string | null>(
    initialMainPlayerTrackRunId
  );
  const [selectedMotionSmoothingRunId, setSelectedMotionSmoothingRunId] = useState<string | null>(
    initialMotionSmoothingRunId
  );
  const [selectedCourtRunId, setSelectedCourtRunId] = useState<string | null>(initialCourtRunId);
  const [selectedHomographyRunId, setSelectedHomographyRunId] = useState<string | null>(
    initialHomographyRunId
  );
  const [selectedProjectionDiagnosticRunId, setSelectedProjectionDiagnosticRunId] = useState<
    string | null
  >(initialProjectionDiagnosticRunId);
  const [selectedCourtProjectionRunId, setSelectedCourtProjectionRunId] = useState<
    string | null
  >(initialCourtProjectionRunId);
  const [selectedBallTrajectoryRunId, setSelectedBallTrajectoryRunId] = useState<string | null>(
    initialBallTrajectoryRunId
  );
  const [selectedEventCandidateRunId, setSelectedEventCandidateRunId] = useState<string | null>(
    initialEventCandidateRunId
  );
  const [replayLayerPreset, setReplayLayerPreset] =
    useState<ReplayLayerPreset>(initialReplayLayerPreset);
  const [showDetections, setShowDetections] = useState(initialLayerPresetState.showDetections);
  const [showTracklets, setShowTracklets] = useState(initialLayerPresetState.showTracklets);
  const [showPoses, setShowPoses] = useState(initialLayerPresetState.showPoses);
  const [showMainPlayerTracks, setShowMainPlayerTracks] = useState(
    initialLayerPresetState.showMainPlayerTracks
  );
  const [showSmoothedBall, setShowSmoothedBall] = useState(
    initialLayerPresetState.showSmoothedBall
  );
  const [showSmoothedPlayerBoxes, setShowSmoothedPlayerBoxes] = useState(
    initialLayerPresetState.showSmoothedPlayerBoxes
  );
  const [showSmoothedPoses, setShowSmoothedPoses] = useState(
    initialLayerPresetState.showSmoothedPoses
  );
  const [detectionDisplayMode, setDetectionDisplayMode] =
    useState<ReplayOverlayDisplayMode>(initialLayerPresetState.detectionDisplayMode);
  const [trackletDisplayMode, setTrackletDisplayMode] =
    useState<ReplayOverlayDisplayMode>(initialLayerPresetState.trackletDisplayMode);
  const [smoothedMotionDisplayMode, setSmoothedMotionDisplayMode] =
    useState<ReplayOverlayDisplayMode>(initialLayerPresetState.smoothedMotionDisplayMode);
  const [poseVisualStyle, setPoseVisualStyle] =
    useState<ReplayPoseVisualStyle>(initialLayerPresetState.poseVisualStyle);
  const [showTrackletPaths, setShowTrackletPaths] = useState(
    initialLayerPresetState.showTrackletPaths
  );
  const [showRawCourtKeypoints, setShowRawCourtKeypoints] = useState(
    initialLayerPresetState.showRawCourtKeypoints
  );
  const [showCourtKeypoints, setShowCourtKeypoints] = useState(
    initialLayerPresetState.showCourtKeypoints
  );
  const [showCourtLines, setShowCourtLines] = useState(initialLayerPresetState.showCourtLines);
  const [showCameraView, setShowCameraView] = useState(initialLayerPresetState.showCameraView);
  const [showHomography, setShowHomography] = useState(initialLayerPresetState.showHomography);
  const [showProjectionDiagnostics, setShowProjectionDiagnostics] = useState(
    initialLayerPresetState.showProjectionDiagnostics
  );
  const [showBallCourtProjection, setShowBallCourtProjection] = useState(
    initialLayerPresetState.showBallCourtProjection
  );
  const [showMainPlayerCourtProjection, setShowMainPlayerCourtProjection] = useState(
    initialLayerPresetState.showMainPlayerCourtProjection
  );
  const [showBallCourtTrajectory, setShowBallCourtTrajectory] = useState(
    initialLayerPresetState.showBallCourtTrajectory
  );
  const [showEventCandidates, setShowEventCandidates] = useState(
    initialLayerPresetState.showEventCandidates
  );
  const [courtTemporalPersistence, setCourtTemporalPersistence] =
    useState<ReplayCourtTemporalPersistence>(initialLayerPresetState.courtTemporalPersistence);
  const [courtPersistenceMaxGapMs, setCourtPersistenceMaxGapMs] = useState(
    initialCourtPersistenceMaxGapMs
  );
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

  const applyReplayLayerPresetState = useCallback(
    (preset: ReplayLayerPreset, context: ReplayLayerPresetContext) => {
      const presetState = applyLayerPreset(preset, context);
      setReplayLayerPreset(preset);
      setShowDetections(presetState.showDetections);
      setShowTracklets(presetState.showTracklets);
      setShowTrackletPaths(presetState.showTrackletPaths);
      setShowPoses(presetState.showPoses);
      setShowMainPlayerTracks(presetState.showMainPlayerTracks);
      setShowSmoothedBall(presetState.showSmoothedBall);
      setShowSmoothedPlayerBoxes(presetState.showSmoothedPlayerBoxes);
      setShowSmoothedPoses(presetState.showSmoothedPoses);
      setShowRawCourtKeypoints(presetState.showRawCourtKeypoints);
      setShowCourtKeypoints(presetState.showCourtKeypoints);
      setShowCourtLines(presetState.showCourtLines);
      setShowCameraView(presetState.showCameraView);
      setShowHomography(presetState.showHomography);
      setShowProjectionDiagnostics(presetState.showProjectionDiagnostics);
      setShowBallCourtProjection(presetState.showBallCourtProjection);
      setShowMainPlayerCourtProjection(presetState.showMainPlayerCourtProjection);
      setShowBallCourtTrajectory(presetState.showBallCourtTrajectory);
      setShowEventCandidates(presetState.showEventCandidates);
      setDetectionDisplayMode(presetState.detectionDisplayMode);
      setTrackletDisplayMode(presetState.trackletDisplayMode);
      setSmoothedMotionDisplayMode(presetState.smoothedMotionDisplayMode);
      setPoseVisualStyle(presetState.poseVisualStyle);
      setCourtTemporalPersistence(presetState.courtTemporalPersistence);
      chunkCache.current.clear();
      setSelectedEvidence(null);
    },
    []
  );

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
    setSelectedMainPlayerTrackRunId(initialMainPlayerTrackRunId);
  }, [initialMainPlayerTrackRunId]);

  useEffect(() => {
    setSelectedMotionSmoothingRunId(initialMotionSmoothingRunId);
  }, [initialMotionSmoothingRunId]);

  useEffect(() => {
    setSelectedCourtRunId(initialCourtRunId);
  }, [initialCourtRunId]);

  useEffect(() => {
    setSelectedHomographyRunId(initialHomographyRunId);
  }, [initialHomographyRunId]);

  useEffect(() => {
    setSelectedProjectionDiagnosticRunId(initialProjectionDiagnosticRunId);
  }, [initialProjectionDiagnosticRunId]);

  useEffect(() => {
    setSelectedCourtProjectionRunId(initialCourtProjectionRunId);
  }, [initialCourtProjectionRunId]);

  useEffect(() => {
    setSelectedBallTrajectoryRunId(initialBallTrajectoryRunId);
  }, [initialBallTrajectoryRunId]);

  useEffect(() => {
    setSelectedEventCandidateRunId(initialEventCandidateRunId);
  }, [initialEventCandidateRunId]);

  useEffect(() => {
    applyReplayLayerPresetState(initialReplayLayerPreset, initialLayerPresetContext);
  }, [applyReplayLayerPresetState, initialLayerPresetContext, initialReplayLayerPreset]);

  useEffect(() => {
    setReplayMode(initialMode);
  }, [initialMode]);

  useEffect(() => {
    setCourtTemporalPersistence(initialCourtTemporalPersistence);
  }, [initialCourtTemporalPersistence]);

  useEffect(() => {
    setCourtPersistenceMaxGapMs(initialCourtPersistenceMaxGapMs);
  }, [initialCourtPersistenceMaxGapMs]);

  const currentLayerPresetContext = useMemo(
    () =>
      presetContextFromRunIds({
        detectionRunId: selectedDetectionRunId,
        trackletRunId: selectedTrackletRunId,
        poseRunId: selectedPoseRunId,
        mainPlayerTrackRunId: selectedMainPlayerTrackRunId,
        motionSmoothingRunId: selectedMotionSmoothingRunId,
        courtRunId: selectedCourtRunId,
        homographyRunId: selectedHomographyRunId,
        projectionDiagnosticRunId: selectedProjectionDiagnosticRunId,
        courtProjectionRunId: selectedCourtProjectionRunId,
        ballTrajectoryRunId: selectedBallTrajectoryRunId,
        eventCandidateRunId: selectedEventCandidateRunId
      }),
    [
      selectedBallTrajectoryRunId,
      selectedCourtProjectionRunId,
      selectedCourtRunId,
      selectedDetectionRunId,
      selectedHomographyRunId,
      selectedMainPlayerTrackRunId,
      selectedMotionSmoothingRunId,
      selectedPoseRunId,
      selectedProjectionDiagnosticRunId,
      selectedTrackletRunId,
      selectedEventCandidateRunId
    ]
  );

  const handleReplayLayerPresetChange = useCallback(
    (preset: ReplayLayerPreset) => {
      applyReplayLayerPresetState(preset, currentLayerPresetContext);
    },
    [applyReplayLayerPresetState, currentLayerPresetContext]
  );

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
    if (showMainPlayerTracks && selectedMainPlayerTrackRunId !== null) {
      layers.push("main_player_tracks");
    }
    if (showSmoothedBall && selectedMotionSmoothingRunId !== null) {
      layers.push("smoothed_ball");
    }
    if (showSmoothedPlayerBoxes && selectedMotionSmoothingRunId !== null) {
      layers.push("smoothed_player_boxes");
    }
    if (showSmoothedPoses && selectedMotionSmoothingRunId !== null) {
      layers.push("smoothed_pose");
    }
    if ((showCourtKeypoints || showRawCourtKeypoints) && selectedCourtRunId !== null) {
      layers.push("court_keypoints");
    }
    if (showCourtLines && selectedCourtRunId !== null) {
      layers.push("court_lines");
    }
    if (showCameraView && selectedCourtRunId !== null) {
      layers.push("camera_view");
    }
    if (showHomography && selectedHomographyRunId !== null) {
      layers.push("homography_candidates");
    }
    if (showProjectionDiagnostics && selectedProjectionDiagnosticRunId !== null) {
      layers.push("projection_diagnostics");
    }
    if (showBallCourtProjection && selectedCourtProjectionRunId !== null) {
      layers.push("ball_court_projection");
    }
    if (showMainPlayerCourtProjection && selectedCourtProjectionRunId !== null) {
      layers.push("main_player_court_projection");
    }
    if (showBallCourtTrajectory && selectedBallTrajectoryRunId !== null) {
      layers.push("ball_court_trajectory");
    }
    if (showEventCandidates && selectedEventCandidateRunId !== null) {
      layers.push("event_candidates");
    }
    return layers;
  }, [
    selectedBallTrajectoryRunId,
    selectedCourtRunId,
    selectedCourtProjectionRunId,
    selectedDetectionRunId,
    selectedHomographyRunId,
    selectedMainPlayerTrackRunId,
    selectedMotionSmoothingRunId,
    selectedPoseRunId,
    selectedProjectionDiagnosticRunId,
    selectedEventCandidateRunId,
    selectedTrackletRunId,
    showCameraView,
    showBallCourtProjection,
    showCourtKeypoints,
    showRawCourtKeypoints,
    showCourtLines,
    showDetections,
    showHomography,
    showMainPlayerTracks,
    showPoses,
    showProjectionDiagnostics,
    showMainPlayerCourtProjection,
    showBallCourtTrajectory,
    showEventCandidates,
    showSmoothedBall,
    showSmoothedPlayerBoxes,
    showSmoothedPoses,
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
    selectedMainPlayerTrackRunId ?? "none",
    selectedMotionSmoothingRunId ?? "none",
    selectedCourtRunId ?? "none",
    selectedHomographyRunId ?? "none",
    selectedProjectionDiagnosticRunId ?? "none",
    selectedCourtProjectionRunId ?? "none",
    selectedBallTrajectoryRunId ?? "none",
    selectedEventCandidateRunId ?? "none",
    courtTemporalPersistence,
    courtPersistenceMaxGapMs,
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
      mainPlayerTrackRunId: selectedMainPlayerTrackRunId,
      motionSmoothingRunId: selectedMotionSmoothingRunId,
      courtRunId: selectedCourtRunId,
      homographyRunId: selectedHomographyRunId,
      projectionDiagnosticRunId: selectedProjectionDiagnosticRunId,
      courtProjectionRunId: selectedCourtProjectionRunId,
      ballTrajectoryRunId: selectedBallTrajectoryRunId,
      eventCandidateRunId: selectedEventCandidateRunId,
      courtTemporalPersistence,
      courtPersistenceMaxGapMs,
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
    courtPersistenceMaxGapMs,
    courtTemporalPersistence,
    currentChunkEnd,
    currentChunkStart,
    enabledLayers.length,
    layersParam,
    replayInfo.media_id,
    selectedCourtRunId,
    selectedCourtProjectionRunId,
    selectedBallTrajectoryRunId,
    selectedDetectionRunId,
    selectedHomographyRunId,
    selectedMainPlayerTrackRunId,
    selectedMotionSmoothingRunId,
    selectedPoseRunId,
    selectedProjectionDiagnosticRunId,
    selectedEventCandidateRunId,
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
      mainPlayerTrackRunId: selectedMainPlayerTrackRunId,
      motionSmoothingRunId: selectedMotionSmoothingRunId,
      courtRunId: selectedCourtRunId,
      homographyRunId: selectedHomographyRunId,
      projectionDiagnosticRunId: selectedProjectionDiagnosticRunId,
      courtProjectionRunId: selectedCourtProjectionRunId,
      ballTrajectoryRunId: selectedBallTrajectoryRunId,
      eventCandidateRunId: selectedEventCandidateRunId,
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
  }, [
    replayInfo.media_id,
    selectedBallTrajectoryRunId,
    selectedCourtRunId,
    selectedCourtProjectionRunId,
    selectedDetectionRunId,
    selectedHomographyRunId,
    selectedMainPlayerTrackRunId,
    selectedMotionSmoothingRunId,
    selectedPoseRunId,
    selectedProjectionDiagnosticRunId,
    selectedEventCandidateRunId,
    selectedTrackletRunId
  ]);

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
      if (item.item_type === "main_player_track_assignment") {
        setSelectedEvidence({ kind: "main_player_track_timeline", item });
        return;
      }
      if (isSmoothedMotionTimelineItem(item)) {
        setSelectedEvidence({ kind: "smoothed_motion_timeline", item });
        return;
      }
      if (item.item_type === "court_keypoint") {
        setSelectedEvidence({ kind: "court_keypoint_timeline", item });
        return;
      }
      if (item.item_type === "court_line") {
        setSelectedEvidence({ kind: "court_line_timeline", item });
        return;
      }
      if (item.item_type === "camera_view") {
        setSelectedEvidence({ kind: "camera_view_timeline", item });
        return;
      }
      if (item.item_type === "homography_candidate") {
        setSelectedEvidence({ kind: "homography_candidate_timeline", item });
        return;
      }
      if (item.item_type === "projection_diagnostic") {
        setSelectedEvidence({ kind: "projection_diagnostic_timeline", item });
        return;
      }
      if (
        item.item_type === "ball_court_projection_candidate" ||
        item.item_type === "main_player_court_projection_candidate"
      ) {
        setSelectedEvidence({ kind: "court_projection_timeline", item });
        return;
      }
      if (item.item_type === "ball_trajectory_court_candidate") {
        setSelectedEvidence({ kind: "ball_trajectory_timeline", item });
        return;
      }
      if (item.item_type === "hit_candidate" || item.item_type === "bounce_candidate") {
        setSelectedEvidence({ kind: "event_candidate_timeline", item });
        return;
      }
      if (item.item_type === "annotation") {
        setSelectedEvidence({ kind: "annotation", item });
      }
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
  const mainPlayerTracks = filterMainPlayerTracksAvailableAt(
    overlayState.chunk?.main_player_tracks ?? [],
    streamAvailableUntilMs
  );
  const smoothedBall = filterSmoothedBallAvailableAt(
    overlayState.chunk?.smoothed_ball ?? [],
    streamAvailableUntilMs
  );
  const smoothedPlayerBoxes = filterSmoothedPlayerBoxesAvailableAt(
    overlayState.chunk?.smoothed_player_boxes ?? [],
    streamAvailableUntilMs
  );
  const smoothedPoses = filterSmoothedPosesAvailableAt(
    overlayState.chunk?.smoothed_pose ?? [],
    streamAvailableUntilMs
  );
  const courtKeypoints = filterCourtKeypointsAvailableAt(
    overlayState.chunk?.court_keypoints ?? [],
    streamAvailableUntilMs
  );
  const courtLines = filterCourtLinesAvailableAt(
    overlayState.chunk?.court_lines ?? [],
    streamAvailableUntilMs
  );
  const cameraViews = filterCameraViewsAvailableAt(
    overlayState.chunk?.camera_view ?? [],
    streamAvailableUntilMs
  );
  const homographyCandidates = filterHomographyCandidatesAvailableAt(
    overlayState.chunk?.homography_candidates ?? [],
    streamAvailableUntilMs
  );
  const projectionDiagnostics = filterProjectionDiagnosticsAvailableAt(
    overlayState.chunk?.projection_diagnostics ?? [],
    streamAvailableUntilMs
  );
  const ballCourtProjection = filterBallCourtProjectionAvailableAt(
    overlayState.chunk?.ball_court_projection ?? [],
    streamAvailableUntilMs
  );
  const mainPlayerCourtProjection = filterMainPlayerCourtProjectionAvailableAt(
    overlayState.chunk?.main_player_court_projection ?? [],
    streamAvailableUntilMs
  );
  const ballCourtTrajectory = filterBallCourtTrajectoryAvailableAt(
    overlayState.chunk?.ball_court_trajectory ?? [],
    streamAvailableUntilMs
  );
  const eventCandidates = filterEventCandidatesAvailableAt(
    [
      ...(overlayState.chunk?.hit_candidates ?? []),
      ...(overlayState.chunk?.bounce_candidates ?? [])
    ],
    streamAvailableUntilMs
  );
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
  const selectedMainPlayerTrackObservationId =
    selectedEvidence?.kind === "main_player_track"
      ? selectedEvidence.item.observation_id
      : selectedEvidence?.kind === "main_player_track_timeline"
        ? selectedEvidence.item.observation_id
        : null;
  const selectedSmoothedMotionObservationId =
    selectedEvidence?.kind === "smoothed_ball" ||
    selectedEvidence?.kind === "smoothed_player_box" ||
    selectedEvidence?.kind === "smoothed_pose" ||
    selectedEvidence?.kind === "smoothed_motion_timeline"
      ? selectedEvidence.item.observation_id
      : null;
  const selectedCourtObservationId = courtSelectedObservationId(selectedEvidence);
  const selectedCourtProjectionObservationId =
    selectedEvidence?.kind === "ball_court_projection" ||
    selectedEvidence?.kind === "main_player_court_projection" ||
    selectedEvidence?.kind === "court_projection_timeline" ||
    selectedEvidence?.kind === "ball_trajectory" ||
    selectedEvidence?.kind === "ball_trajectory_timeline" ||
    selectedEvidence?.kind === "event_candidate" ||
    selectedEvidence?.kind === "event_candidate_timeline"
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
            <span className="mono replay-media-id" title={replayInfo.media_id}>
              {replayInfo.media_id}
            </span>
          </div>
        </div>
        <div className="meta-line viewer-summary-badges">
          <span className="mini-pill">{replayInfo.frame_time_mode} frame/time</span>
          <span className="mini-pill">{detections.length} detection overlays</span>
          <span className="mini-pill">{tracklets.length} tracklet candidates</span>
          <span className="mini-pill">{mainPlayerTracks.length} main player track labels</span>
          <span className="mini-pill">{poses.length} pose observations</span>
          <span className="mini-pill">
            {smoothedBall.length + smoothedPlayerBoxes.length + smoothedPoses.length} smoothed
            candidates
          </span>
          <span className="mini-pill">
            {courtKeypoints.length +
              courtLines.length +
              homographyCandidates.length +
              projectionDiagnostics.length} court overlays
          </span>
          <span className="mini-pill">
            {ballCourtProjection.length + mainPlayerCourtProjection.length} court projection
            candidates
          </span>
          <span className="mini-pill">{eventCandidates.length} event candidates</span>
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
              displayMode={detectionDisplayMode}
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
              displayMode={trackletDisplayMode}
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
              showPaths={showTrackletPaths}
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
              poseVisualStyle={poseVisualStyle}
              poses={poses}
              replayInfo={replayInfo}
              selectedObservationId={selectedPoseObservationId}
            />
            <ReplayMainPlayerTrackOverlayLayer
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              enabled={showMainPlayerTracks && selectedMainPlayerTrackRunId !== null}
              error={overlayState.error}
              isLoading={overlayState.loading}
              onSelectTrackAssignment={(item) => {
                setSelectedEvidence({ kind: "main_player_track", item });
              }}
              replayInfo={replayInfo}
              selectedObservationId={selectedMainPlayerTrackObservationId}
              tracks={mainPlayerTracks}
            />
            <ReplaySmoothedMotionOverlayLayer
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              enabledBall={showSmoothedBall && selectedMotionSmoothingRunId !== null}
              enabledPlayerBoxes={
                showSmoothedPlayerBoxes && selectedMotionSmoothingRunId !== null
              }
              enabledPoses={showSmoothedPoses && selectedMotionSmoothingRunId !== null}
              error={overlayState.error}
              displayMode={smoothedMotionDisplayMode}
              isLoading={overlayState.loading}
              onSelectSmoothedBall={(item) => {
                setSelectedEvidence({ kind: "smoothed_ball", item });
              }}
              onSelectSmoothedPlayerBox={(item) => {
                setSelectedEvidence({ kind: "smoothed_player_box", item });
              }}
              onSelectSmoothedPose={(item) => {
                setSelectedEvidence({ kind: "smoothed_pose", item });
              }}
              replayInfo={replayInfo}
              poseVisualStyle={poseVisualStyle}
              selectedObservationId={selectedSmoothedMotionObservationId}
              smoothedBall={smoothedBall}
              smoothedPlayerBoxes={smoothedPlayerBoxes}
              smoothedPoses={smoothedPoses}
            />
            <ReplayCourtOverlayLayer
              cameraViews={cameraViews}
              courtKeypoints={courtKeypoints}
              courtLines={courtLines}
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              error={overlayState.error}
              homographyCandidates={homographyCandidates}
              isLoading={overlayState.loading}
              onSelectCameraView={(item) => {
                setSelectedEvidence({ kind: "camera_view", item });
              }}
              onSelectCourtKeypoint={(item) => {
                setSelectedEvidence({ kind: "court_keypoint", item });
              }}
              onSelectCourtLine={(item) => {
                setSelectedEvidence({ kind: "court_line", item });
              }}
              onSelectHomography={(item) => {
                setSelectedEvidence({ kind: "homography_candidate", item });
              }}
              onSelectProjectionDiagnostic={(item) => {
                setSelectedEvidence({ kind: "projection_diagnostic", item });
              }}
              projectionDiagnostics={projectionDiagnostics}
              replayInfo={replayInfo}
              selectedObservationId={selectedCourtObservationId}
              showCameraView={showCameraView && selectedCourtRunId !== null}
              showCourtKeypoints={showCourtKeypoints && selectedCourtRunId !== null}
              showRawCourtKeypoints={showRawCourtKeypoints && selectedCourtRunId !== null}
              showCourtLines={showCourtLines && selectedCourtRunId !== null}
              showHomography={showHomography && selectedHomographyRunId !== null}
              showProjectionDiagnostics={
                showProjectionDiagnostics && selectedProjectionDiagnosticRunId !== null
              }
            />
            <ReplayEventCandidateVideoOverlay
              currentFrame={playback.frameNumber}
              currentTimestampMs={playback.timestampMs}
              enabled={showEventCandidates && selectedEventCandidateRunId !== null}
              error={overlayState.error}
              eventCandidates={eventCandidates}
              isLoading={overlayState.loading}
              onSelectEventCandidate={(item) => {
                setSelectedEvidence({ kind: "event_candidate", item });
              }}
              replayInfo={replayInfo}
              selectedObservationId={selectedCourtProjectionObservationId}
            />
          </ReplayVideoPlayer>
          <ReplayCourtProjectionMiniMap
            ballProjections={ballCourtProjection}
            ballTrajectories={ballCourtTrajectory}
            eventCandidates={eventCandidates}
            currentFrame={playback.frameNumber}
            currentTimestampMs={playback.timestampMs}
            mainPlayerProjections={mainPlayerCourtProjection}
            onSelectBallProjection={(item) => {
              setSelectedEvidence({ kind: "ball_court_projection", item });
            }}
            onSelectBallTrajectory={(item) => {
              setSelectedEvidence({ kind: "ball_trajectory", item });
            }}
            onSelectEventCandidate={(item) => {
              setSelectedEvidence({ kind: "event_candidate", item });
            }}
            onSelectMainPlayerProjection={(item) => {
              setSelectedEvidence({ kind: "main_player_court_projection", item });
            }}
            selectedObservationId={selectedCourtProjectionObservationId}
            showBall={showBallCourtProjection && selectedCourtProjectionRunId !== null}
            showBallTrajectory={showBallCourtTrajectory && selectedBallTrajectoryRunId !== null}
            showEventCandidates={showEventCandidates && selectedEventCandidateRunId !== null}
            showPlayers={showMainPlayerCourtProjection && selectedCourtProjectionRunId !== null}
          />
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
            ballTrajectoryRuns={replayInfo.available_runs.ball_trajectory}
            courtRuns={replayInfo.available_runs.court}
            courtProjectionRuns={replayInfo.available_runs.court_projection}
            detectionRuns={replayInfo.available_runs.detection}
            eventCandidateRuns={replayInfo.available_runs.event_candidate}
            homographyRuns={replayInfo.available_runs.homography}
            mainPlayerTrackRuns={replayInfo.available_runs.main_player_track}
            motionSmoothingRuns={replayInfo.available_runs.motion_smoothing}
            projectionDiagnosticRuns={replayInfo.available_runs.projection_diagnostic}
            replayLayerPreset={replayLayerPreset}
            onReplayLayerPresetChange={handleReplayLayerPresetChange}
            onSelectedCourtRunChange={(runId) => {
              setSelectedCourtRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedDetectionRunChange={(runId) => {
              setSelectedDetectionRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedHomographyRunChange={(runId) => {
              setSelectedHomographyRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedMainPlayerTrackRunChange={(runId) => {
              setSelectedMainPlayerTrackRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedMotionSmoothingRunChange={(runId) => {
              setSelectedMotionSmoothingRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedProjectionDiagnosticRunChange={(runId) => {
              setSelectedProjectionDiagnosticRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedCourtProjectionRunChange={(runId) => {
              setSelectedCourtProjectionRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedBallTrajectoryRunChange={(runId) => {
              setSelectedBallTrajectoryRunId(runId);
              setSelectedEvidence(null);
            }}
            onSelectedEventCandidateRunChange={(runId) => {
              setSelectedEventCandidateRunId(runId);
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
            onDetectionDisplayModeChange={setDetectionDisplayMode}
            onToggleCameraView={setShowCameraView}
            onToggleCourtKeypoints={setShowCourtKeypoints}
            onToggleRawCourtKeypoints={setShowRawCourtKeypoints}
            onToggleCourtLines={setShowCourtLines}
            onToggleHomography={setShowHomography}
            onToggleMainPlayerTracks={setShowMainPlayerTracks}
            onToggleProjectionDiagnostics={setShowProjectionDiagnostics}
            onToggleBallCourtProjection={setShowBallCourtProjection}
            onToggleBallCourtTrajectory={setShowBallCourtTrajectory}
            onToggleEventCandidates={setShowEventCandidates}
            onToggleMainPlayerCourtProjection={setShowMainPlayerCourtProjection}
            onTogglePoses={setShowPoses}
            onPoseVisualStyleChange={setPoseVisualStyle}
            onToggleSmoothedBall={setShowSmoothedBall}
            onToggleSmoothedPlayerBoxes={setShowSmoothedPlayerBoxes}
            onToggleSmoothedPoses={setShowSmoothedPoses}
            onSmoothedMotionDisplayModeChange={setSmoothedMotionDisplayMode}
            onCourtTemporalPersistenceChange={(mode) => {
              chunkCache.current.clear();
              setCourtTemporalPersistence(mode);
              setSelectedEvidence(null);
            }}
            onCourtPersistenceMaxGapMsChange={(maxGapMs) => {
              chunkCache.current.clear();
              setCourtPersistenceMaxGapMs(maxGapMs);
              setSelectedEvidence(null);
            }}
            onTrackletDisplayModeChange={setTrackletDisplayMode}
            onToggleTrackletPaths={setShowTrackletPaths}
            onToggleTracklets={setShowTracklets}
            poseRuns={replayInfo.available_runs.pose}
            selectedCourtRunId={selectedCourtRunId}
            selectedDetectionRunId={selectedDetectionRunId}
            selectedHomographyRunId={selectedHomographyRunId}
            selectedMainPlayerTrackRunId={selectedMainPlayerTrackRunId}
            selectedMotionSmoothingRunId={selectedMotionSmoothingRunId}
            selectedPoseRunId={selectedPoseRunId}
            selectedProjectionDiagnosticRunId={selectedProjectionDiagnosticRunId}
            selectedCourtProjectionRunId={selectedCourtProjectionRunId}
            selectedBallTrajectoryRunId={selectedBallTrajectoryRunId}
            selectedEventCandidateRunId={selectedEventCandidateRunId}
            selectedTrackletRunId={selectedTrackletRunId}
            showBallCourtProjection={showBallCourtProjection}
            showBallCourtTrajectory={showBallCourtTrajectory}
            showEventCandidates={showEventCandidates}
            showCameraView={showCameraView}
            showCourtKeypoints={showCourtKeypoints}
            showRawCourtKeypoints={showRawCourtKeypoints}
            showCourtLines={showCourtLines}
            courtTemporalPersistence={courtTemporalPersistence}
            courtPersistenceMaxGapMs={courtPersistenceMaxGapMs}
            showDetections={showDetections}
            showHomography={showHomography}
            showMainPlayerTracks={showMainPlayerTracks}
            poseVisualStyle={poseVisualStyle}
            showPoses={showPoses}
            showProjectionDiagnostics={showProjectionDiagnostics}
            showMainPlayerCourtProjection={showMainPlayerCourtProjection}
            showSmoothedBall={showSmoothedBall}
            smoothedMotionDisplayMode={smoothedMotionDisplayMode}
            showSmoothedPlayerBoxes={showSmoothedPlayerBoxes}
            showSmoothedPoses={showSmoothedPoses}
            detectionDisplayMode={detectionDisplayMode}
            trackletDisplayMode={trackletDisplayMode}
            showTrackletPaths={showTrackletPaths}
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
              main_player_tracks: showMainPlayerTracks,
              smoothed_motion: showSmoothedBall || showSmoothedPlayerBoxes || showSmoothedPoses,
              court_keypoints: showCourtKeypoints || showRawCourtKeypoints,
              court_lines: showCourtLines,
              camera_view: showCameraView,
              homography_candidates: showHomography,
              projection_diagnostics: showProjectionDiagnostics,
              court_projection: showBallCourtProjection || showMainPlayerCourtProjection,
              ball_trajectory: showBallCourtTrajectory,
              event_candidates: showEventCandidates,
              annotations: true
            }}
            onSelectItem={handleTimelineItemSelect}
            selectedItemKey={selectedTimelineKey}
            timeline={timelineState.timeline}
          />
          <SelectedRunContext
            replayInfo={replayInfo}
            selectedCourtRunId={selectedCourtRunId}
            selectedDetectionRunId={selectedDetectionRunId}
            selectedHomographyRunId={selectedHomographyRunId}
            selectedMainPlayerTrackRunId={selectedMainPlayerTrackRunId}
            selectedMotionSmoothingRunId={selectedMotionSmoothingRunId}
            selectedPoseRunId={selectedPoseRunId}
            selectedCourtProjectionRunId={selectedCourtProjectionRunId}
            selectedBallTrajectoryRunId={selectedBallTrajectoryRunId}
            selectedEventCandidateRunId={selectedEventCandidateRunId}
            selectedProjectionDiagnosticRunId={selectedProjectionDiagnosticRunId}
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
  ballTrajectoryRuns,
  detectionRuns,
  trackletRuns,
  poseRuns,
  mainPlayerTrackRuns,
  motionSmoothingRuns,
  courtRuns,
  homographyRuns,
  projectionDiagnosticRuns,
  courtProjectionRuns,
  eventCandidateRuns,
  replayLayerPreset,
  selectedDetectionRunId,
  selectedTrackletRunId,
  selectedPoseRunId,
  selectedMainPlayerTrackRunId,
  selectedMotionSmoothingRunId,
  selectedCourtRunId,
  selectedHomographyRunId,
  selectedProjectionDiagnosticRunId,
  selectedCourtProjectionRunId,
  selectedBallTrajectoryRunId,
  selectedEventCandidateRunId,
  showDetections,
  detectionDisplayMode,
  showTracklets,
  trackletDisplayMode,
  showTrackletPaths,
  showPoses,
  poseVisualStyle,
  showMainPlayerTracks,
  showSmoothedBall,
  smoothedMotionDisplayMode,
  showSmoothedPlayerBoxes,
  showSmoothedPoses,
  showRawCourtKeypoints,
  showCourtKeypoints,
  showCourtLines,
  courtTemporalPersistence,
  courtPersistenceMaxGapMs,
  showCameraView,
  showHomography,
  showProjectionDiagnostics,
  showBallCourtProjection,
  showMainPlayerCourtProjection,
  showBallCourtTrajectory,
  showEventCandidates,
  onReplayLayerPresetChange,
  onSelectedDetectionRunChange,
  onSelectedTrackletRunChange,
  onSelectedPoseRunChange,
  onSelectedMainPlayerTrackRunChange,
  onSelectedMotionSmoothingRunChange,
  onSelectedCourtRunChange,
  onSelectedHomographyRunChange,
  onSelectedProjectionDiagnosticRunChange,
  onSelectedCourtProjectionRunChange,
  onSelectedBallTrajectoryRunChange,
  onSelectedEventCandidateRunChange,
  onToggleDetections,
  onDetectionDisplayModeChange,
  onToggleTracklets,
  onTrackletDisplayModeChange,
  onToggleTrackletPaths,
  onTogglePoses,
  onPoseVisualStyleChange,
  onToggleMainPlayerTracks,
  onToggleSmoothedBall,
  onToggleSmoothedPlayerBoxes,
  onToggleSmoothedPoses,
  onSmoothedMotionDisplayModeChange,
  onToggleRawCourtKeypoints,
  onToggleCourtKeypoints,
  onToggleCourtLines,
  onCourtTemporalPersistenceChange,
  onCourtPersistenceMaxGapMsChange,
  onToggleCameraView,
  onToggleHomography,
  onToggleProjectionDiagnostics,
  onToggleBallCourtProjection,
  onToggleMainPlayerCourtProjection,
  onToggleBallCourtTrajectory,
  onToggleEventCandidates
}: {
  ballTrajectoryRuns: ReplayRunSummary[];
  detectionRuns: ReplayRunSummary[];
  trackletRuns: ReplayRunSummary[];
  poseRuns: ReplayRunSummary[];
  mainPlayerTrackRuns: ReplayRunSummary[];
  motionSmoothingRuns: ReplayRunSummary[];
  courtRuns: ReplayRunSummary[];
  homographyRuns: ReplayRunSummary[];
  projectionDiagnosticRuns: ReplayRunSummary[];
  courtProjectionRuns: ReplayRunSummary[];
  eventCandidateRuns: ReplayRunSummary[];
  replayLayerPreset: ReplayLayerPreset;
  selectedDetectionRunId: string | null;
  selectedTrackletRunId: string | null;
  selectedPoseRunId: string | null;
  selectedMainPlayerTrackRunId: string | null;
  selectedMotionSmoothingRunId: string | null;
  selectedCourtRunId: string | null;
  selectedHomographyRunId: string | null;
  selectedProjectionDiagnosticRunId: string | null;
  selectedCourtProjectionRunId: string | null;
  selectedBallTrajectoryRunId: string | null;
  selectedEventCandidateRunId: string | null;
  showDetections: boolean;
  detectionDisplayMode: ReplayOverlayDisplayMode;
  showTracklets: boolean;
  trackletDisplayMode: ReplayOverlayDisplayMode;
  showTrackletPaths: boolean;
  showPoses: boolean;
  poseVisualStyle: ReplayPoseVisualStyle;
  showMainPlayerTracks: boolean;
  showSmoothedBall: boolean;
  smoothedMotionDisplayMode: ReplayOverlayDisplayMode;
  showSmoothedPlayerBoxes: boolean;
  showSmoothedPoses: boolean;
  showRawCourtKeypoints: boolean;
  showCourtKeypoints: boolean;
  showCourtLines: boolean;
  courtTemporalPersistence: ReplayCourtTemporalPersistence;
  courtPersistenceMaxGapMs: number;
  showCameraView: boolean;
  showHomography: boolean;
  showProjectionDiagnostics: boolean;
  showBallCourtProjection: boolean;
  showMainPlayerCourtProjection: boolean;
  showBallCourtTrajectory: boolean;
  showEventCandidates: boolean;
  onReplayLayerPresetChange: (preset: ReplayLayerPreset) => void;
  onSelectedDetectionRunChange: (runId: string | null) => void;
  onSelectedTrackletRunChange: (runId: string | null) => void;
  onSelectedPoseRunChange: (runId: string | null) => void;
  onSelectedMainPlayerTrackRunChange: (runId: string | null) => void;
  onSelectedMotionSmoothingRunChange: (runId: string | null) => void;
  onSelectedCourtRunChange: (runId: string | null) => void;
  onSelectedHomographyRunChange: (runId: string | null) => void;
  onSelectedProjectionDiagnosticRunChange: (runId: string | null) => void;
  onSelectedCourtProjectionRunChange: (runId: string | null) => void;
  onSelectedBallTrajectoryRunChange: (runId: string | null) => void;
  onSelectedEventCandidateRunChange: (runId: string | null) => void;
  onToggleDetections: (enabled: boolean) => void;
  onDetectionDisplayModeChange: (mode: ReplayOverlayDisplayMode) => void;
  onToggleTracklets: (enabled: boolean) => void;
  onTrackletDisplayModeChange: (mode: ReplayOverlayDisplayMode) => void;
  onToggleTrackletPaths: (enabled: boolean) => void;
  onTogglePoses: (enabled: boolean) => void;
  onPoseVisualStyleChange: (style: ReplayPoseVisualStyle) => void;
  onToggleMainPlayerTracks: (enabled: boolean) => void;
  onToggleSmoothedBall: (enabled: boolean) => void;
  onToggleSmoothedPlayerBoxes: (enabled: boolean) => void;
  onToggleSmoothedPoses: (enabled: boolean) => void;
  onSmoothedMotionDisplayModeChange: (mode: ReplayOverlayDisplayMode) => void;
  onToggleRawCourtKeypoints: (enabled: boolean) => void;
  onToggleCourtKeypoints: (enabled: boolean) => void;
  onToggleCourtLines: (enabled: boolean) => void;
  onCourtTemporalPersistenceChange: (mode: ReplayCourtTemporalPersistence) => void;
  onCourtPersistenceMaxGapMsChange: (maxGapMs: number) => void;
  onToggleCameraView: (enabled: boolean) => void;
  onToggleHomography: (enabled: boolean) => void;
  onToggleProjectionDiagnostics: (enabled: boolean) => void;
  onToggleBallCourtProjection: (enabled: boolean) => void;
  onToggleMainPlayerCourtProjection: (enabled: boolean) => void;
  onToggleBallCourtTrajectory: (enabled: boolean) => void;
  onToggleEventCandidates: (enabled: boolean) => void;
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Replay Overlay Layers</h2>
        <span className="mini-pill">persisted evidence</span>
      </div>
      <div className="panel-body replay-controls">
        <ReplayLayerPresetSelect
          onChange={onReplayLayerPresetChange}
          value={replayLayerPreset}
        />
        <LayerToggle
          checked={showDetections}
          label="Show detection observations"
          onChange={onToggleDetections}
        />
        <DisplayModeSelect
          label="Detection display"
          onChange={onDetectionDisplayModeChange}
          value={detectionDisplayMode}
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
        <DisplayModeSelect
          label="Tracklet point display"
          onChange={onTrackletDisplayModeChange}
          value={trackletDisplayMode}
        />
        <LayerToggle
          checked={showTrackletPaths}
          label="Show tracklet trail/path"
          onChange={onToggleTrackletPaths}
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
        <PoseVisualStyleSelect onChange={onPoseVisualStyleChange} value={poseVisualStyle} />
        <RunSelect
          label="Pose run"
          onChange={onSelectedPoseRunChange}
          runs={poseRuns}
          selectedRunId={selectedPoseRunId}
        />
        <LayerToggle
          checked={showMainPlayerTracks}
          label="Show main player track candidates"
          onChange={onToggleMainPlayerTracks}
        />
        <RunSelect
          label="Main player track run"
          onChange={onSelectedMainPlayerTrackRunChange}
          runs={mainPlayerTrackRuns}
          selectedRunId={selectedMainPlayerTrackRunId}
        />
        <LayerToggle
          checked={showSmoothedBall}
          label="Show smoothed ball candidate"
          onChange={onToggleSmoothedBall}
        />
        <LayerToggle
          checked={showSmoothedPlayerBoxes}
          label="Show smoothed main player boxes"
          onChange={onToggleSmoothedPlayerBoxes}
        />
        <LayerToggle
          checked={showSmoothedPoses}
          label="Show smoothed pose candidates"
          onChange={onToggleSmoothedPoses}
        />
        <DisplayModeSelect
          label="Smoothed motion display"
          onChange={onSmoothedMotionDisplayModeChange}
          value={smoothedMotionDisplayMode}
        />
        <RunSelect
          label="Motion smoothing run"
          onChange={onSelectedMotionSmoothingRunChange}
          runs={motionSmoothingRuns}
          selectedRunId={selectedMotionSmoothingRunId}
        />
        <LayerToggle
          checked={showRawCourtKeypoints}
          label="Show raw TOM v1 court keypoints"
          onChange={onToggleRawCourtKeypoints}
        />
        <LayerToggle
          checked={showCourtKeypoints}
          label="Show mapped TOM v3 court keypoints"
          onChange={onToggleCourtKeypoints}
        />
        <LayerToggle
          checked={showCourtLines}
          label="Show court line evidence"
          onChange={onToggleCourtLines}
        />
        <LayerToggle
          checked={showCameraView}
          label="Show camera/view evidence"
          onChange={onToggleCameraView}
        />
        <CourtTemporalPersistenceSelect
          onChange={onCourtTemporalPersistenceChange}
          value={courtTemporalPersistence}
        />
        <label className="select-row">
          <span>Court carry-forward max gap</span>
          <input
            min={0}
            onChange={(event) => {
              const parsed = Number.parseInt(event.target.value, 10);
              onCourtPersistenceMaxGapMsChange(Number.isFinite(parsed) ? Math.max(0, parsed) : 0);
            }}
            step={100}
            type="number"
            value={courtPersistenceMaxGapMs}
          />
        </label>
        <RunSelect
          label="Court evidence run"
          onChange={onSelectedCourtRunChange}
          runs={courtRuns}
          selectedRunId={selectedCourtRunId}
        />
        <LayerToggle
          checked={showHomography}
          label="Show homography candidates"
          onChange={onToggleHomography}
        />
        <RunSelect
          label="Homography run"
          onChange={onSelectedHomographyRunChange}
          runs={homographyRuns}
          selectedRunId={selectedHomographyRunId}
        />
        <LayerToggle
          checked={showProjectionDiagnostics}
          label="Show projection diagnostics"
          onChange={onToggleProjectionDiagnostics}
        />
        <RunSelect
          label="Projection diagnostic run"
          onChange={onSelectedProjectionDiagnosticRunChange}
          runs={projectionDiagnosticRuns}
          selectedRunId={selectedProjectionDiagnosticRunId}
        />
        <LayerToggle
          checked={showBallCourtProjection}
          label="Show ball court projection candidates"
          onChange={onToggleBallCourtProjection}
        />
        <LayerToggle
          checked={showMainPlayerCourtProjection}
          label="Show main player court projection candidates"
          onChange={onToggleMainPlayerCourtProjection}
        />
        <RunSelect
          label="Court projection run"
          onChange={onSelectedCourtProjectionRunChange}
          runs={courtProjectionRuns}
          selectedRunId={selectedCourtProjectionRunId}
        />
        <LayerToggle
          checked={showBallCourtTrajectory}
          label="Show ball trajectory court candidate"
          onChange={onToggleBallCourtTrajectory}
        />
        <RunSelect
          label="Ball trajectory run"
          onChange={onSelectedBallTrajectoryRunChange}
          runs={ballTrajectoryRuns}
          selectedRunId={selectedBallTrajectoryRunId}
        />
        <LayerToggle
          checked={showEventCandidates}
          label="Show hit/bounce candidate evidence"
          onChange={onToggleEventCandidates}
        />
        <RunSelect
          label="Event candidate run"
          onChange={onSelectedEventCandidateRunChange}
          runs={eventCandidateRuns}
          selectedRunId={selectedEventCandidateRunId}
        />
        <p className="evidence-note">
          Overlays are synchronized persisted evidence. Court geometry layers are candidates for
          review; event-candidate layers are not hit, bounce, in/out, or scoring truth.
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

function DisplayModeSelect({
  label,
  value,
  onChange
}: {
  label: string;
  value: ReplayOverlayDisplayMode;
  onChange: (mode: ReplayOverlayDisplayMode) => void;
}) {
  return (
    <label className="select-row">
      <span>{label}</span>
      <select
        onChange={(event) => onChange(event.target.value as ReplayOverlayDisplayMode)}
        value={value}
      >
        <option value="current_only">Current only</option>
        <option value="short_trail">Short trail</option>
        <option value="full_trail">Full trail</option>
      </select>
    </label>
  );
}

function ReplayLayerPresetSelect({
  value,
  onChange
}: {
  value: ReplayLayerPreset;
  onChange: (preset: ReplayLayerPreset) => void;
}) {
  return (
    <label className="select-row">
      <span>Replay view preset</span>
      <select onChange={(event) => onChange(event.target.value as ReplayLayerPreset)} value={value}>
        <option value="operator">Operator view</option>
        <option value="debug">Debug / audit view</option>
      </select>
    </label>
  );
}

function PoseVisualStyleSelect({
  value,
  onChange
}: {
  value: ReplayPoseVisualStyle;
  onChange: (style: ReplayPoseVisualStyle) => void;
}) {
  return (
    <label className="select-row">
      <span>Pose visual style</span>
      <select
        onChange={(event) => onChange(event.target.value as ReplayPoseVisualStyle)}
        value={value}
      >
        <option value="limbs_only">Limbs only</option>
        <option value="limbs_and_joints">Limbs + joints</option>
        <option value="joints_only">Joints only/debug</option>
      </select>
    </label>
  );
}

function CourtTemporalPersistenceSelect({
  value,
  onChange
}: {
  value: ReplayCourtTemporalPersistence;
  onChange: (mode: ReplayCourtTemporalPersistence) => void;
}) {
  return (
    <label className="select-row">
      <span>Court geometry temporal persistence</span>
      <select
        onChange={(event) => onChange(event.target.value as ReplayCourtTemporalPersistence)}
        value={value}
      >
        <option value="carry_forward">Carry forward latest candidate</option>
        <option value="off">Off</option>
      </select>
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
  const selectedRunHasSummary =
    selectedRunId !== null && runs.some((run) => run.run_id === selectedRunId);

  return (
    <label className="select-row">
      <span>{label}</span>
      <select onChange={(event) => onChange(event.target.value || null)} value={selectedRunId ?? ""}>
        <option value="">Select a run</option>
        {selectedRunId !== null && !selectedRunHasSummary ? (
          <option value={selectedRunId}>URL-selected run {selectedRunId}</option>
        ) : null}
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
        <RunGroup
          title="Main player track candidates"
          runs={replayInfo.available_runs.main_player_track}
        />
        <RunGroup
          title="Motion smoothing candidates"
          runs={replayInfo.available_runs.motion_smoothing}
        />
        <RunGroup title="Pose observations" runs={replayInfo.available_runs.pose} />
        <RunGroup title="Court evidence" runs={replayInfo.available_runs.court} />
        <RunGroup title="Homography candidates" runs={replayInfo.available_runs.homography} />
        <RunGroup
          title="Projection diagnostics"
          runs={replayInfo.available_runs.projection_diagnostic}
        />
        <RunGroup
          title="Court projection candidates"
          runs={replayInfo.available_runs.court_projection}
        />
        <RunGroup
          title="Ball trajectory court candidates"
          runs={replayInfo.available_runs.ball_trajectory}
        />
        <RunGroup
          title="Hit/bounce event candidates"
          runs={replayInfo.available_runs.event_candidate}
        />
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
  selectedPoseRunId,
  selectedMainPlayerTrackRunId,
  selectedMotionSmoothingRunId,
  selectedCourtRunId,
  selectedHomographyRunId,
  selectedProjectionDiagnosticRunId,
  selectedCourtProjectionRunId,
  selectedBallTrajectoryRunId,
  selectedEventCandidateRunId
}: {
  replayInfo: ReplayInfo;
  selectedDetectionRunId: string | null;
  selectedTrackletRunId: string | null;
  selectedPoseRunId: string | null;
  selectedMainPlayerTrackRunId: string | null;
  selectedMotionSmoothingRunId: string | null;
  selectedCourtRunId: string | null;
  selectedHomographyRunId: string | null;
  selectedProjectionDiagnosticRunId: string | null;
  selectedCourtProjectionRunId: string | null;
  selectedBallTrajectoryRunId: string | null;
  selectedEventCandidateRunId: string | null;
}) {
  const selected = [
    ["detection", selectedDetectionRunId, replayInfo.available_runs.detection],
    ["tracklet candidate", selectedTrackletRunId, replayInfo.available_runs.tracklet],
    ["pose observation", selectedPoseRunId, replayInfo.available_runs.pose],
    [
      "main player track candidate",
      selectedMainPlayerTrackRunId,
      replayInfo.available_runs.main_player_track
    ],
    [
      "motion smoothing candidate",
      selectedMotionSmoothingRunId,
      replayInfo.available_runs.motion_smoothing
    ],
    ["court evidence", selectedCourtRunId, replayInfo.available_runs.court],
    ["homography candidate", selectedHomographyRunId, replayInfo.available_runs.homography],
    [
      "projection diagnostic",
      selectedProjectionDiagnosticRunId,
      replayInfo.available_runs.projection_diagnostic
    ],
    [
      "court projection candidate",
      selectedCourtProjectionRunId,
      replayInfo.available_runs.court_projection
    ],
    [
      "ball trajectory court candidate",
      selectedBallTrajectoryRunId,
      replayInfo.available_runs.ball_trajectory
    ],
    [
      "hit/bounce event candidate",
      selectedEventCandidateRunId,
      replayInfo.available_runs.event_candidate
    ]
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
          Selected runs provide synchronized detection observations, tracklet candidates, pose
          keypoint evidence, and court geometry evidence. They do not confirm tennis events, court
          truth, or object identity.
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
            Click a replay bbox, track point, candidate path, pose skeleton, or court evidence to
            inspect persisted evidence.
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
        {item.track_candidate_id ? (
          <DetailRow label="track candidate" value={item.track_candidate_id} />
        ) : null}
        {item.track_role_candidate ? (
          <DetailRow label="track role candidate" value={item.track_role_candidate} />
        ) : null}
        {item.track_assignment_observation_id ? (
          <DetailRow
            label="track assignment observation"
            value={item.track_assignment_observation_id}
          />
        ) : null}
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Pose observation selected from the evidence timeline. Track-linked poses are candidate
          visual subject evidence only; they do not establish identity, strokes, movement, or
          biomechanics.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "main_player_track" ||
    selectedEvidence.kind === "main_player_track_timeline"
  ) {
    const item = selectedEvidence.item;
    const badge =
      "label" in item
        ? item.label
        : "display_label" in item
          ? item.display_label
          : "main player track";
    return (
      <EvidencePanel title="Selected Main Player Track Candidate" badge={badge}>
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="track candidate id" value={item.track_candidate_id ?? "n/a"} />
        <DetailRow label="track role candidate" value={item.track_role_candidate ?? "n/a"} />
        <DetailRow label="assignment score" value={formatConfidence(item.assignment_score)} />
        <DetailRow label="assignment method" value={item.assignment_method ?? "n/a"} />
        {"track_lock_state" in item ? (
          <DetailRow label="track lock state" value={item.track_lock_state ?? "n/a"} />
        ) : null}
        {"source_track_candidate_observation_id" in item ? (
          <DetailRow
            label="track candidate observation"
            value={item.source_track_candidate_observation_id ?? "n/a"}
          />
        ) : null}
        <DetailRow
          label="source subject candidate"
          value={item.source_subject_candidate_observation_id ?? "n/a"}
        />
        <DetailRow
          label="source detection"
          value={item.source_detection_observation_id ?? "n/a"}
        />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="candidate_track_only" value={item.candidate_track_only ? "true" : "false"} />
        <DetailRow label="not_identity_truth" value={item.not_identity_truth ? "true" : "false"} />
        <DetailRow label="observation_only" value={item.observation_only ? "true" : "false"} />
        <DetailRow label="no_adjudication" value={item.no_adjudication ? "true" : "false"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Main player track candidate. This is a visual subject-track assignment only; it is not a
          player identity, name, server role, or accepted player track.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "smoothed_ball" ||
    selectedEvidence.kind === "smoothed_player_box" ||
    selectedEvidence.kind === "smoothed_pose" ||
    selectedEvidence.kind === "smoothed_motion_timeline"
  ) {
    const item = selectedEvidence.item;
    const displayType =
      "overlay_type" in item ? item.overlay_type : item.item_type;
    const title =
      displayType === "smoothed_ball_position_candidate"
        ? "Selected Smoothed Ball Candidate"
        : displayType === "smoothed_main_player_box_candidate"
          ? "Selected Smoothed Main Player Box"
          : "Selected Smoothed Pose Candidate";
    return (
      <EvidencePanel title={title} badge="smoothed candidate">
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="smoothing method" value={item.smoothing_method ?? "n/a"} />
        {"confidence" in item ? (
          <DetailRow label="confidence" value={formatConfidence(item.confidence)} />
        ) : null}
        {"pose_confidence" in item ? (
          <DetailRow label="pose confidence" value={formatConfidence(item.pose_confidence)} />
        ) : null}
        {"source_detection_run_id" in item ? (
          <DetailRow
            label="source detection run"
            value={item.source_detection_run_id ?? "n/a"}
          />
        ) : null}
        {"source_tracklet_run_id" in item ? (
          <DetailRow
            label="source tracklet run"
            value={item.source_tracklet_run_id ?? "n/a"}
          />
        ) : null}
        {"source_main_player_track_run_id" in item ? (
          <DetailRow
            label="source main player track run"
            value={item.source_main_player_track_run_id ?? "n/a"}
          />
        ) : null}
        {"source_pose_run_id" in item ? (
          <DetailRow label="source pose run" value={item.source_pose_run_id ?? "n/a"} />
        ) : null}
        {"track_candidate_id" in item ? (
          <DetailRow label="track candidate" value={item.track_candidate_id ?? "n/a"} />
        ) : null}
        {"track_role_candidate" in item ? (
          <DetailRow label="track role candidate" value={item.track_role_candidate ?? "n/a"} />
        ) : null}
        <DetailRow
          label="source observations"
          value={item.source_observation_ids.length.toString()}
        />
        <DetailRow
          label="smoothed_candidate_only"
          value={item.smoothed_candidate_only ? "true" : "false"}
        />
        <DetailRow label="observation_only" value={item.observation_only ? "true" : "false"} />
        <DetailRow label="no_adjudication" value={item.no_adjudication ? "true" : "false"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Smoothed replay candidate evidence only. It is derived from raw observations for visual
          stability and does not establish ball truth, pose truth, player identity, bounce, hit,
          in/out, point, or score.
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "court_keypoint" || selectedEvidence.kind === "court_keypoint_timeline") {
    const item = selectedEvidence.item;
    const rawPointCount =
      "raw_tom_v1_keypoints" in item ? item.raw_tom_v1_keypoints?.length ?? 0 : null;
    const preprocessingMode = "preprocessing_mode" in item ? item.preprocessing_mode : null;
    const coordinateInterpretation =
      "coordinate_interpretation" in item ? item.coordinate_interpretation : null;
    const mappingVersion = "mapping_version" in item ? item.mapping_version : null;
    const inferredKeypoints =
      "inferred_tom_v3_keypoints" in item ? item.inferred_tom_v3_keypoints ?? [] : [];
    const calibrationWarning =
      "calibration_warning" in item ? item.calibration_warning : null;
    return (
      <EvidencePanel title="Selected Court Keypoint Evidence" badge="court keypoints">
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="schema" value={`${item.court_keypoint_schema} / ${item.schema_version}`} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow
          label="keypoints"
          value={`${item.keypoints_present_count} present / ${item.keypoints_missing_count} missing`}
        />
        <DetailRow label="mean confidence" value={formatConfidence(item.mean_keypoint_confidence)} />
        <DetailRow label="source" value={courtSourceDisplayLabel(item)} />
        <DetailRow label="raw TOM v1 points" value={rawPointCount?.toString() ?? "n/a"} />
        <DetailRow label="preprocessing mode" value={preprocessingMode ?? "n/a"} />
        <DetailRow
          label="coordinate interpretation"
          value={coordinateInterpretation ?? "n/a"}
        />
        <DetailRow label="mapping version" value={mappingVersion ?? "n/a"} />
        <DetailRow
          label="inferred keypoints"
          value={inferredKeypoints.length > 0 ? inferredKeypoints.join(", ") : "n/a"}
        />
        <TemporalDisplayDetails item={item} />
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
          {calibrationWarning ??
            "Court keypoint evidence only. It is not a confirmed court model and does not imply bounce, in/out, point, or score."}
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "court_line" || selectedEvidence.kind === "court_line_timeline") {
    const item = selectedEvidence.item;
    return (
      <EvidencePanel title="Selected Court Line Evidence" badge="court lines">
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="line count" value={item.line_count.toString()} />
        <DetailRow label="line classes" value={(item.line_classes ?? []).join(", ") || "n/a"} />
        <DetailRow label="mean confidence" value={formatConfidence(item.mean_line_confidence)} />
        <DetailRow label="source" value={courtSourceDisplayLabel(item)} />
        <TemporalDisplayDetails item={item} />
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
          Court line evidence only. It is not a confirmed court model and does not imply bounce,
          in/out, point, or score.
        </p>
      </EvidencePanel>
    );
  }

  if (selectedEvidence.kind === "camera_view" || selectedEvidence.kind === "camera_view_timeline") {
    const item = selectedEvidence.item;
    return (
      <EvidencePanel title="Selected Camera/View Evidence" badge={item.view_label}>
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="view label" value={item.view_label} />
        <DetailRow label="confidence" value={formatConfidence(item.view_confidence)} />
        <DetailRow label="motion hint" value={item.camera_motion_hint ?? "n/a"} />
        <DetailRow label="stability" value={formatConfidence(item.stability_score)} />
        <DetailRow label="cut likelihood" value={formatConfidence(item.cut_likelihood)} />
        <DetailRow label="source" value={courtSourceDisplayLabel(item)} />
        <DetailRow label="model registry id" value={item.model_registry_id ?? "n/a"} />
        <DetailRow label="runtime config id" value={item.runtime_config_id ?? "n/a"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Camera/view evidence only. It is geometry context and not a confirmed camera state or
          homography decision.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "homography_candidate" ||
    selectedEvidence.kind === "homography_candidate_timeline"
  ) {
    const item = selectedEvidence.item;
    return (
      <EvidencePanel title="Selected Homography Candidate" badge={item.status}>
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow label="template" value={`${item.template_name} / ${item.template_version}`} />
        <DetailRow label="matrix direction" value={item.matrix_direction} />
        <DetailRow label="source points" value={item.source_point_count?.toString() ?? "n/a"} />
        <DetailRow label="source lines" value={item.source_line_count?.toString() ?? "n/a"} />
        <DetailRow
          label="mean reprojection error"
          value={item.reprojection_error_mean?.toString() ?? "n/a"}
        />
        <DetailRow label="confidence" value={formatConfidence(item.confidence)} />
        <TemporalDisplayDetails item={item} />
        {"source_court_keypoint_observation_id" in item ? (
          <>
            <DetailRow
              label="source keypoint id"
              value={item.source_court_keypoint_observation_id ?? "n/a"}
            />
            <DetailRow
              label="source line id"
              value={item.source_court_line_observation_id ?? "n/a"}
            />
            <DetailRow
              label="source camera/view id"
              value={item.source_camera_view_observation_id ?? "n/a"}
            />
          </>
        ) : null}
        <DetailRow label="source" value={courtSourceDisplayLabel(item)} />
        <DetailRow label="model registry id" value={item.model_registry_id ?? "n/a"} />
        <DetailRow label="runtime config id" value={item.runtime_config_id ?? "n/a"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Homography candidate evidence only. It is not a final court model and does not imply
          bounce, in/out, player position, point, or score.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "projection_diagnostic" ||
    selectedEvidence.kind === "projection_diagnostic_timeline"
  ) {
    const item = selectedEvidence.item;
    const projectedKeypoints =
      "projected_template_keypoints" in item
        ? item.projected_template_keypoints.length
        : item.projected_keypoint_count;
    const projectedLines =
      "projected_template_lines" in item
        ? item.projected_template_lines.length
        : item.projected_line_count;
    return (
      <EvidencePanel title="Selected Projection Diagnostic" badge={item.status}>
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow
          label="source homography id"
          value={item.source_homography_candidate_observation_id}
        />
        <DetailRow label="projected keypoints" value={projectedKeypoints?.toString() ?? "n/a"} />
        <DetailRow label="projected lines" value={projectedLines?.toString() ?? "n/a"} />
        <DetailRow label="confidence" value={formatConfidence(item.confidence)} />
        <DetailRow label="source" value={courtSourceDisplayLabel(item)} />
        <TemporalDisplayDetails item={item} />
        <DetailRow label="model registry id" value={item.model_registry_id ?? "n/a"} />
        <DetailRow label="runtime config id" value={item.runtime_config_id ?? "n/a"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Projection diagnostic evidence only. It projects a court template for review and does not
          project ball/player detections or imply bounce, in/out, point, or score.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "ball_court_projection" ||
    selectedEvidence.kind === "main_player_court_projection" ||
    selectedEvidence.kind === "court_projection_timeline"
  ) {
    const item = selectedEvidence.item;
    const isBall =
      selectedEvidence.kind === "ball_court_projection" ||
      ("item_type" in item && item.item_type === "ball_court_projection_candidate");
    return (
      <EvidencePanel
        title={
          isBall
            ? "Selected Ball Court Projection Candidate"
            : "Selected Main Player Court Projection Candidate"
        }
        badge="court projection"
      >
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow
          label="court point"
          value={`${item.court_point.x.toFixed(4)}, ${item.court_point.y.toFixed(4)}`}
        />
        <DetailRow label="coordinate space" value={item.court_coordinate_space} />
        <DetailRow label="projection method" value={item.projection_method ?? "n/a"} />
        {"image_point" in item ? (
          <DetailRow
            label="image point"
            value={
              item.image_point === null
                ? "n/a"
                : `${item.image_point.x.toFixed(2)}, ${item.image_point.y.toFixed(2)}`
            }
          />
        ) : null}
        {"image_anchor" in item ? (
          <DetailRow
            label="image anchor"
            value={
              item.image_anchor === null
                ? "n/a"
                : `${item.image_anchor.anchor_type}: ${item.image_anchor.x.toFixed(2)}, ${item.image_anchor.y.toFixed(2)}`
            }
          />
        ) : null}
        {"track_candidate_id" in item ? (
          <DetailRow label="track candidate" value={item.track_candidate_id ?? "n/a"} />
        ) : null}
        {"track_role_candidate" in item ? (
          <DetailRow label="track role candidate" value={item.track_role_candidate ?? "n/a"} />
        ) : null}
        {"source_motion_smoothing_run_id" in item ? (
          <DetailRow
            label="source motion smoothing run"
            value={item.source_motion_smoothing_run_id ?? "n/a"}
          />
        ) : null}
        <DetailRow
          label="source homography id"
          value={item.source_homography_observation_id ?? "n/a"}
        />
        <DetailRow
          label="homography time delta"
          value={
            item.homography_time_delta_ms === null
              ? "n/a"
              : `${item.homography_time_delta_ms} ms`
          }
        />
        <DetailRow
          label="homography carried forward"
          value={item.homography_carried_forward ? "true" : "false"}
        />
        <DetailRow
          label="projection_candidate_only"
          value={item.projection_candidate_only ? "true" : "false"}
        />
        <DetailRow label="not_court_truth" value={item.not_court_truth ? "true" : "false"} />
        <DetailRow label="observation_only" value={item.observation_only ? "true" : "false"} />
        <DetailRow label="no_adjudication" value={item.no_adjudication ? "true" : "false"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Court projection candidate evidence only. It is derived from smoothed image-space
          evidence and a homography candidate; it does not imply bounce, hit, in/out, player
          position truth, point, or score.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "ball_trajectory" ||
    selectedEvidence.kind === "ball_trajectory_timeline"
  ) {
    const item = selectedEvidence.item;
    const diagnostics =
      "diagnostics" in item && item.diagnostics !== undefined ? item.diagnostics : null;
    return (
      <EvidencePanel
        title="Selected Ball Trajectory Court Candidate"
        badge="trajectory candidate"
      >
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="frame range" value={`${item.frame_start}-${item.frame_end}`} />
        <DetailRow
          label="timestamp range"
          value={`${item.timestamp_start_ms}-${item.timestamp_end_ms} ms`}
        />
        <DetailRow label="point count" value={item.point_count.toString()} />
        <DetailRow label="trajectory method" value={item.trajectory_method ?? "n/a"} />
        <DetailRow label="coordinate space" value={item.coordinate_space} />
        <DetailRow
          label="source court projection run"
          value={item.source_court_projection_run_id ?? "n/a"}
        />
        {diagnostics !== null ? (
          <>
            <DetailRow
              label="gap splits"
              value={String(diagnostics.segment_split_count ?? diagnostics.gap_count ?? "n/a")}
            />
            <DetailRow
              label="out-of-template"
              value={String(diagnostics.out_of_template_count ?? "n/a")}
            />
            <DetailRow
              label="homography carry-forward"
              value={String(diagnostics.homography_carried_forward_count ?? "n/a")}
            />
          </>
        ) : null}
        <DetailRow
          label="trajectory_candidate_only"
          value={item.trajectory_candidate_only ? "true" : "false"}
        />
        <DetailRow label="not_ball_truth" value={item.not_ball_truth ? "true" : "false"} />
        <DetailRow
          label="not_bounce_truth"
          value={item.not_bounce_truth ? "true" : "false"}
        />
        <DetailRow label="not_hit_truth" value={item.not_hit_truth ? "true" : "false"} />
        <DetailRow
          label="not_in_out_truth"
          value={item.not_in_out_truth ? "true" : "false"}
        />
        <DetailRow label="observation_only" value={item.observation_only ? "true" : "false"} />
        <DetailRow label="no_adjudication" value={item.no_adjudication ? "true" : "false"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Ball trajectory court candidate evidence only. It is a derived sequence of projected ball
          candidates and does not imply bounce, hit, in/out, point, or score.
        </p>
      </EvidencePanel>
    );
  }

  if (
    selectedEvidence.kind === "event_candidate" ||
    selectedEvidence.kind === "event_candidate_timeline"
  ) {
    const item = selectedEvidence.item;
    const nearestPlayer = "nearest_player" in item ? item.nearest_player : null;
    const trajectoryContext =
      "trajectory_context" in item && item.trajectory_context !== undefined
        ? item.trajectory_context
        : null;
    const title =
      item.candidate_type === "hit_candidate"
        ? "Selected Hit Candidate Evidence"
        : "Selected Bounce Candidate Evidence";
    return (
      <EvidencePanel title={title} badge="event candidate">
        <DetailRow label="observation id" value={item.observation_id} />
        <DetailRow label="run id" value={item.run_id} />
        <DetailRow label="candidate type" value={item.candidate_type} />
        <DetailRow label="frame" value={item.frame_number.toString()} />
        <DetailRow label="timestamp_ms" value={item.timestamp_ms.toString()} />
        <DetailRow
          label="court point"
          value={`${item.court_point.x.toFixed(4)}, ${item.court_point.y.toFixed(4)}`}
        />
        <DetailRow
          label="image point"
          value={
            item.image_point === null
              ? "unavailable"
              : `${item.image_point.x.toFixed(2)}, ${item.image_point.y.toFixed(2)}`
          }
        />
        <DetailRow label="image marker source" value={item.image_marker_source} />
        <DetailRow label="confidence" value={formatConfidence(item.confidence)} />
        <DetailRow label="candidate method" value={item.candidate_method ?? "n/a"} />
        <DetailRow label="classification priority" value={item.classification_priority ?? "n/a"} />
        <DetailRow
          label="court side zone"
          value={String(item.court_side_zone?.side ?? "n/a")}
        />
        <DetailRow
          label="player contact zone"
          value={
            item.player_contact_zone === null || item.player_contact_zone === undefined
              ? "n/a"
              : String(item.player_contact_zone.in_contact_zone ?? "n/a")
          }
        />
        <DetailRow
          label="court landing zone"
          value={
            item.court_landing_zone === null || item.court_landing_zone === undefined
              ? "n/a"
              : String(item.court_landing_zone.landing_zone_candidate ?? "n/a")
          }
        />
        <DetailRow
          label="reclassification"
          value={
            item.candidate_reclassification === null ||
            item.candidate_reclassification === undefined
              ? "n/a"
              : `${String(item.candidate_reclassification.original_candidate_type ?? "n/a")} → ${String(
                  item.candidate_reclassification.final_candidate_type ?? "n/a"
                )}`
          }
        />
        <DetailRow
          label="sequence prior"
          value={
            item.candidate_sequence === null || item.candidate_sequence === undefined
              ? "n/a"
              : `${String(item.candidate_sequence.previous_candidate_type ?? "start")} → expected ${String(
                  item.candidate_sequence.expected_candidate_type ?? "n/a"
                )}`
          }
        />
        <DetailRow
          label="player anchored recall"
          value={
            item.player_anchored_hit_recall === null ||
            item.player_anchored_hit_recall === undefined
              ? "n/a"
              : String(item.player_anchored_hit_recall.enabled ?? "n/a")
          }
        />
        <DetailRow
          label="anchor track role"
          value={
            item.player_anchored_hit_recall === null ||
            item.player_anchored_hit_recall === undefined
              ? "n/a"
              : String(item.player_anchored_hit_recall.anchor_track_role_candidate ?? "n/a")
          }
        />
        <DetailRow
          label="anchor distance"
          value={
            item.player_anchored_hit_recall === null ||
            item.player_anchored_hit_recall === undefined
              ? "n/a"
              : String(item.player_anchored_hit_recall.distance_template_units ?? "n/a")
          }
        />
        <DetailRow
          label="wide-window reversal"
          value={
            item.player_anchored_hit_recall === null ||
            item.player_anchored_hit_recall === undefined
              ? "n/a"
              : `${String(item.player_anchored_hit_recall.vy_before ?? "n/a")} / ${String(
                  item.player_anchored_hit_recall.vy_after ?? "n/a"
                )}`
          }
        />
        {item.player_proximity_gate !== null ? (
          <>
            <DetailRow
              label="player gate found"
              value={item.player_proximity_gate.nearest_player_found ? "true" : "false"}
            />
            <DetailRow
              label="player gate distance"
              value={
                item.player_proximity_gate.distance_template_units === null
                  ? "n/a"
                  : item.player_proximity_gate.distance_template_units.toFixed(4)
              }
            />
            <DetailRow
              label="player gate threshold"
              value={item.player_proximity_gate.threshold.toFixed(4)}
            />
          </>
        ) : null}
        {item.candidate_decision !== null ? (
          <>
            <DetailRow
              label="candidate decision"
              value={item.candidate_decision.selected_candidate_type}
            />
            <DetailRow
              label="suppressed candidate types"
              value={
                item.candidate_decision.suppressed_candidate_types.length > 0
                  ? item.candidate_decision.suppressed_candidate_types.join(", ")
                  : "none"
              }
            />
            <DetailRow label="decision reason" value={item.candidate_decision.reason} />
          </>
        ) : null}
        {item.net_axis_reversal !== null ? (
          <>
            <DetailRow
              label="net-axis reversal"
              value={item.net_axis_reversal.reversal ? "true" : "false"}
            />
            <DetailRow
              label="net-axis vy before/after"
              value={`${item.net_axis_reversal.vy_before ?? "n/a"} / ${
                item.net_axis_reversal.vy_after ?? "n/a"
              }`}
            />
            <DetailRow
              label="net-axis frames"
              value={`${item.net_axis_reversal.previous_frame ?? "n/a"} → ${
                item.net_axis_reversal.current_frame ?? "n/a"
              } → ${item.net_axis_reversal.next_frame ?? "n/a"}`}
            />
          </>
        ) : null}
        {item.vertical_motion_proxy !== null ? (
          <>
            <DetailRow
              label="vertical proxy"
              value={
                item.vertical_motion_proxy.descending_to_ascending
                  ? "descending→ascending"
                  : item.vertical_motion_proxy.status ?? "n/a"
              }
            />
            <DetailRow
              label="image-y before/current/after"
              value={`${item.vertical_motion_proxy.image_y_before ?? "n/a"} / ${
                item.vertical_motion_proxy.image_y_current ?? "n/a"
              } / ${item.vertical_motion_proxy.image_y_after ?? "n/a"}`}
            />
            <DetailRow
              label="image-y delta before/after"
              value={`${item.vertical_motion_proxy.image_vy_before ?? "n/a"} / ${
                item.vertical_motion_proxy.image_vy_after ?? "n/a"
              }`}
            />
          </>
        ) : null}
        {item.speed_reduction !== null ? (
          <>
            <DetailRow
              label="speed reduction"
              value={item.speed_reduction.speed_reduced ? "true" : "false"}
            />
            <DetailRow
              label="speed reduction fraction"
              value={
                item.speed_reduction.speed_reduction_fraction === null
                  ? "n/a"
                  : item.speed_reduction.speed_reduction_fraction.toFixed(4)
              }
            />
          </>
        ) : null}
        <DetailRow
          label="reason codes"
          value={item.reason_codes.length > 0 ? item.reason_codes.join(", ") : "n/a"}
        />
        <DetailRow
          label="source trajectory id"
          value={item.source_ball_trajectory_observation_id ?? "n/a"}
        />
        <DetailRow
          label="source ball projection id"
          value={item.source_ball_court_projection_observation_id ?? "n/a"}
        />
        <DetailRow
          label="source player projection id"
          value={item.source_player_court_projection_observation_id ?? "n/a"}
        />
        {nearestPlayer !== null ? (
          <>
            <DetailRow
              label="nearest player role"
              value={nearestPlayer.track_role_candidate ?? "n/a"}
            />
            <DetailRow
              label="nearest player distance"
              value={nearestPlayer.distance_template_units.toFixed(4)}
            />
            <DetailRow
              label="nearest player time delta"
              value={`${nearestPlayer.time_delta_ms} ms`}
            />
          </>
        ) : null}
        {trajectoryContext !== null ? (
          <>
            <DetailRow
              label="direction delta"
              value={
                trajectoryContext.direction_delta_degrees === undefined
                  ? "n/a"
                  : `${trajectoryContext.direction_delta_degrees.toFixed(2)} deg`
              }
            />
            <DetailRow
              label="speed before/after"
              value={`${trajectoryContext.speed_before ?? "n/a"} / ${
                trajectoryContext.speed_after ?? "n/a"
              }`}
            />
          </>
        ) : null}
        <DetailRow label="candidate_only" value={item.candidate_only ? "true" : "false"} />
        <DetailRow label="not_hit_truth" value={item.not_hit_truth ? "true" : "false"} />
        <DetailRow label="not_bounce_truth" value={item.not_bounce_truth ? "true" : "false"} />
        <DetailRow label="not_in_out_truth" value={item.not_in_out_truth ? "true" : "false"} />
        <DetailRow label="observation_only" value={item.observation_only ? "true" : "false"} />
        <DetailRow label="no_adjudication" value={item.no_adjudication ? "true" : "false"} />
        <a className="quiet-link" href={`/runs/${item.run_id}`}>
          Open source evidence run
        </a>
        <p className="evidence-note">
          Hit/bounce candidate evidence only. These markers are derived from trajectory diagnostics
          and player proximity candidates; they are not hit truth, bounce truth, in/out, point, or
          score.
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
      {pose.subject_context.track_candidate_id ? (
        <DetailRow label="track candidate" value={pose.subject_context.track_candidate_id} />
      ) : null}
      {pose.subject_context.track_role_candidate ? (
        <DetailRow label="track role candidate" value={pose.subject_context.track_role_candidate} />
      ) : null}
      {pose.subject_context.track_assignment_observation_id ? (
        <DetailRow
          label="track assignment observation"
          value={pose.subject_context.track_assignment_observation_id}
        />
      ) : null}
      <a className="quiet-link" href={`/runs/${pose.run_id}`}>
        Open source evidence run
      </a>
      <p className="evidence-note">
        Pose observation. Track-linked poses are candidate visual subject evidence only; they do not
        establish identity, strokes, movement, or biomechanics.
      </p>
    </EvidencePanel>
  );
}

function TemporalDisplayDetails({ item }: { item: ReplayCourtEvidenceSource }) {
  if (!item.temporal_display_mode) {
    return null;
  }
  return (
    <>
      <DetailRow label="temporal display" value={item.temporal_display_mode} />
      <DetailRow label="carried forward" value={item.carried_forward ? "true" : "false"} />
      <DetailRow
        label="source observation"
        value={item.source_observation_id ?? "n/a"}
      />
      <DetailRow
        label="source frame"
        value={item.source_frame_number?.toString() ?? "n/a"}
      />
      <DetailRow
        label="source timestamp_ms"
        value={item.source_observation_timestamp_ms?.toString() ?? "n/a"}
      />
      <DetailRow
        label="current timestamp_ms"
        value={item.current_replay_timestamp_ms?.toString() ?? "n/a"}
      />
      <DetailRow
        label="active window"
        value={`${item.active_from_ms ?? "n/a"} - ${item.active_until_ms ?? "n/a"} ms`}
      />
      <DetailRow
        label="persistence max gap"
        value={item.court_persistence_max_gap_ms?.toString() ?? "n/a"}
      />
      <DetailRow
        label="carry boundary"
        value={item.carry_forward_boundary ?? "n/a"}
      />
      <DetailRow
        label="camera boundary available"
        value={item.camera_view_boundary_available ? "true" : "false"}
      />
      <DetailRow label="not court truth" value={item.not_court_truth ? "true" : "false"} />
    </>
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

function isSmoothedMotionTimelineItem(
  item: ReplayTimelineItem
): item is ReplaySmoothedMotionTimelineItem {
  return (
    item.item_type === "smoothed_ball_position_candidate" ||
    item.item_type === "smoothed_main_player_box_candidate" ||
    item.item_type === "smoothed_pose_candidate"
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
  if (selectedEvidence.kind === "main_player_track") {
    return `main_player_track_assignment:${selectedEvidence.item.observation_id}`;
  }
  if (
    selectedEvidence.kind === "smoothed_ball" ||
    selectedEvidence.kind === "smoothed_player_box" ||
    selectedEvidence.kind === "smoothed_pose"
  ) {
    return `${selectedEvidence.item.overlay_type}:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "court_keypoint") {
    return `court_keypoint:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "court_line") {
    return `court_line:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "camera_view") {
    return `camera_view:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "homography_candidate") {
    return `homography_candidate:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "projection_diagnostic") {
    return `projection_diagnostic:${selectedEvidence.item.observation_id}`;
  }
  if (
    selectedEvidence.kind === "ball_court_projection" ||
    selectedEvidence.kind === "main_player_court_projection"
  ) {
    return `${selectedEvidence.item.overlay_type}:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "ball_trajectory") {
    return `${selectedEvidence.item.overlay_type}:${selectedEvidence.item.observation_id}`;
  }
  if (selectedEvidence.kind === "event_candidate") {
    return `${selectedEvidence.item.overlay_type}:${selectedEvidence.item.observation_id}`;
  }
  return timelineItemKey(selectedEvidence.item);
}

function courtSelectedObservationId(selectedEvidence: SelectedReplayEvidence | null): string | null {
  if (selectedEvidence === null) {
    return null;
  }
  if (
    selectedEvidence.kind === "court_keypoint" ||
    selectedEvidence.kind === "court_line" ||
    selectedEvidence.kind === "camera_view" ||
    selectedEvidence.kind === "homography_candidate" ||
    selectedEvidence.kind === "projection_diagnostic" ||
    selectedEvidence.kind === "court_keypoint_timeline" ||
    selectedEvidence.kind === "court_line_timeline" ||
    selectedEvidence.kind === "camera_view_timeline" ||
    selectedEvidence.kind === "homography_candidate_timeline" ||
    selectedEvidence.kind === "projection_diagnostic_timeline"
  ) {
    return selectedEvidence.item.observation_id;
  }
  return null;
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
  if (run.evidence_source === "main_player_track_assignment") {
    return "main player visual track candidates";
  }
  if (run.evidence_source === "motion_smoothing_candidate" || run.smoothed_candidate_only) {
    return "smoothed replay candidates";
  }
  if (run.evidence_source === "fixture_derived_tracklet") {
    return "fixture-derived tracklet candidates";
  }
  if (run.evidence_source === "fixture_court_evidence") {
    return "fixture court evidence";
  }
  if (run.evidence_source === "homography_candidate" || run.candidate_geometry) {
    return "homography candidate";
  }
  if (run.evidence_source === "projection_diagnostic" || run.diagnostic_geometry) {
    return "projection diagnostic";
  }
  if (run.evidence_source === "court_projection_candidate" || run.projection_candidate_only) {
    return "court projection candidate";
  }
  if (run.evidence_source === "event_candidate" || run.event_candidate_only || run.candidate_only) {
    return "hit/bounce event candidates";
  }
  if (run.geometry_evidence_only) {
    return run.source_label ?? "court geometry evidence";
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
  if (item.candidate_track_only || item.track_candidate_id) {
    return "Main player track candidate pose evidence";
  }
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

function courtSourceDisplayLabel(item: {
  evidence_source?: string;
  source_label?: string | null;
  fixture_court_evidence?: boolean;
  fixture_camera_view_evidence?: boolean;
  real_model_output?: boolean;
  is_real_model_output?: boolean;
  model_output_not_truth?: boolean;
  candidate_geometry?: boolean;
  diagnostic_geometry?: boolean;
  not_ball_player_projection?: boolean;
  uncalibrated_tom_v1_keypoint_mapping?: boolean;
  calibration_warning?: string | null;
}): string {
  if (
    item.diagnostic_geometry ||
    item.evidence_source === "projection_diagnostic" ||
    item.not_ball_player_projection
  ) {
    return "Projection diagnostic";
  }
  if (item.candidate_geometry || item.evidence_source === "homography_candidate") {
    return "Homography candidate";
  }
  if (item.fixture_court_evidence || item.evidence_source === "fixture_court_evidence") {
    return "Fixture court evidence";
  }
  if (
    item.fixture_camera_view_evidence ||
    item.evidence_source === "fixture_camera_view_evidence"
  ) {
    return "Fixture camera/view evidence";
  }
  if (
    item.real_model_output ||
    item.is_real_model_output ||
    item.evidence_source === "real_model_output"
  ) {
    return item.source_label ?? "Real court keypoint model output";
  }
  return item.source_label ?? "Court geometry evidence";
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
