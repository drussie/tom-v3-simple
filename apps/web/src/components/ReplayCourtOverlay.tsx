"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import {
  activeReplayCameraViews,
  activeReplayCourtKeypoints,
  activeReplayCourtLines,
  activeReplayHomographyCandidates,
  activeReplayProjectionDiagnostics,
  imagePixelPointToOverlayPoint,
  projectTemplatePointWithMatrix
} from "../lib/replayOverlays";
import type {
  HomographyMatrix3x3,
  ReplayCameraViewOverlay,
  ReplayCourtKeypoint,
  ReplayCourtKeypointOverlay,
  ReplayCourtLineOverlay,
  ReplayCourtTemplate,
  ReplayHomographyCandidateOverlay,
  ReplayInfo,
  ReplayProjectionDiagnosticOverlay
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayCourtOverlayProps {
  replayInfo: ReplayInfo;
  courtKeypoints: ReplayCourtKeypointOverlay[];
  courtLines: ReplayCourtLineOverlay[];
  cameraViews: ReplayCameraViewOverlay[];
  homographyCandidates: ReplayHomographyCandidateOverlay[];
  projectionDiagnostics: ReplayProjectionDiagnosticOverlay[];
  currentTimestampMs: number;
  currentFrame: number;
  showCourtKeypoints: boolean;
  showRawCourtKeypoints: boolean;
  showCourtLines: boolean;
  showCameraView: boolean;
  showHomography: boolean;
  showProjectionDiagnostics: boolean;
  isLoading: boolean;
  error: string | null;
  selectedObservationId: string | null;
  onSelectCourtKeypoint: (item: ReplayCourtKeypointOverlay) => void;
  onSelectCourtLine: (item: ReplayCourtLineOverlay) => void;
  onSelectCameraView: (item: ReplayCameraViewOverlay) => void;
  onSelectHomography: (item: ReplayHomographyCandidateOverlay) => void;
  onSelectProjectionDiagnostic: (item: ReplayProjectionDiagnosticOverlay) => void;
  holdMs?: number;
}

interface OverlaySize {
  width: number;
  height: number;
}

const fallbackTemplate: ReplayCourtTemplate = {
  template_name: "tennis_court_template_normalized_v0",
  template_version: "v0",
  target_coordinate_space: "court_template_2d",
  keypoints: [
    { name: "near_left_baseline_corner", x: 0, y: 0 },
    { name: "near_right_baseline_corner", x: 1, y: 0 },
    { name: "far_left_baseline_corner", x: 0, y: 1 },
    { name: "far_right_baseline_corner", x: 1, y: 1 },
    { name: "left_net_post", x: 0, y: 0.5 },
    { name: "right_net_post", x: 1, y: 0.5 },
    { name: "service_line_t_near_left", x: 0.25, y: 0.35 },
    { name: "service_line_t_near_right", x: 0.75, y: 0.35 },
    { name: "service_line_t_far_left", x: 0.25, y: 0.65 },
    { name: "service_line_t_far_right", x: 0.75, y: 0.65 },
    { name: "center_mark_near", x: 0.5, y: 0 },
    { name: "center_mark_far", x: 0.5, y: 1 }
  ],
  lines: [
    {
      line_class: "baseline_near",
      start_keypoint: "near_left_baseline_corner",
      end_keypoint: "near_right_baseline_corner"
    },
    {
      line_class: "baseline_far",
      start_keypoint: "far_left_baseline_corner",
      end_keypoint: "far_right_baseline_corner"
    },
    {
      line_class: "sideline_left",
      start_keypoint: "near_left_baseline_corner",
      end_keypoint: "far_left_baseline_corner"
    },
    {
      line_class: "sideline_right",
      start_keypoint: "near_right_baseline_corner",
      end_keypoint: "far_right_baseline_corner"
    },
    {
      line_class: "service_line_near",
      start_keypoint: "service_line_t_near_left",
      end_keypoint: "service_line_t_near_right"
    },
    {
      line_class: "service_line_far",
      start_keypoint: "service_line_t_far_left",
      end_keypoint: "service_line_t_far_right"
    },
    {
      line_class: "center_service_line",
      start_keypoint: "service_line_t_near_left",
      end_keypoint: "service_line_t_far_left"
    },
    {
      line_class: "net_line",
      start_keypoint: "left_net_post",
      end_keypoint: "right_net_post"
    }
  ]
};

export function ReplayCourtOverlay({
  replayInfo,
  courtKeypoints,
  courtLines,
  cameraViews,
  homographyCandidates,
  projectionDiagnostics,
  currentTimestampMs,
  currentFrame,
  showCourtKeypoints,
  showRawCourtKeypoints,
  showCourtLines,
  showCameraView,
  showHomography,
  showProjectionDiagnostics,
  isLoading,
  error,
  selectedObservationId,
  onSelectCourtKeypoint,
  onSelectCourtLine,
  onSelectCameraView,
  onSelectHomography,
  onSelectProjectionDiagnostic,
  holdMs = 250
}: ReplayCourtOverlayProps) {
  const overlayRef = useRef<HTMLDivElement | null>(null);
  const [overlaySize, setOverlaySize] = useState<OverlaySize>({ width: 0, height: 0 });

  useEffect(() => {
    const overlay = overlayRef.current;
    if (overlay === null) {
      return;
    }
    const updateSize = () => {
      const rect = overlay.getBoundingClientRect();
      setOverlaySize({ width: rect.width, height: rect.height });
    };
    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(overlay);
    return () => observer.disconnect();
  }, []);

  const activeKeypoints = useMemo(
    () => activeReplayCourtKeypoints(courtKeypoints, currentTimestampMs, currentFrame, holdMs),
    [courtKeypoints, currentFrame, currentTimestampMs, holdMs]
  );
  const activeLines = useMemo(
    () => activeReplayCourtLines(courtLines, currentTimestampMs, currentFrame, holdMs),
    [courtLines, currentFrame, currentTimestampMs, holdMs]
  );
  const activeCameraViews = useMemo(
    () => activeReplayCameraViews(cameraViews, currentTimestampMs, currentFrame, holdMs),
    [cameraViews, currentFrame, currentTimestampMs, holdMs]
  );
  const activeHomographies = useMemo(
    () =>
      activeReplayHomographyCandidates(
        homographyCandidates,
        currentTimestampMs,
        currentFrame,
        holdMs
      ),
    [currentFrame, currentTimestampMs, holdMs, homographyCandidates]
  );
  const activeProjectionDiagnostics = useMemo(
    () =>
      activeReplayProjectionDiagnostics(
        projectionDiagnostics,
        currentTimestampMs,
        currentFrame,
        holdMs
      ),
    [currentFrame, currentTimestampMs, holdMs, projectionDiagnostics]
  );
  const anyLayerEnabled =
    showCourtKeypoints ||
    showRawCourtKeypoints ||
    showCourtLines ||
    showCameraView ||
    showHomography ||
    showProjectionDiagnostics;
  const totalCount =
    courtKeypoints.length +
    courtLines.length +
    cameraViews.length +
    homographyCandidates.length +
    projectionDiagnostics.length;
  const activeCount =
    (showCourtKeypoints ? activeKeypoints.length : 0) +
    (showRawCourtKeypoints ? activeKeypoints.length : 0) +
    (showCourtLines ? activeLines.length : 0) +
    (showCameraView ? activeCameraViews.length : 0) +
    (showHomography ? activeHomographies.length : 0) +
    (showProjectionDiagnostics ? activeProjectionDiagnostics.length : 0);
  const status = overlayStatus({
    enabled: anyLayerEnabled,
    isLoading,
    error,
    activeCount,
    totalCount
  });

  return (
    <div className="replay-overlay-layer court" ref={overlayRef}>
      {anyLayerEnabled ? (
        <svg className="replay-vector-layer" role="presentation">
          {showHomography
            ? activeHomographies.map((homography) => (
                <HomographyCandidateGroup
                  homography={homography}
                  key={homography.observation_id}
                  onSelect={onSelectHomography}
                  overlaySize={overlaySize}
                  replayInfo={replayInfo}
                  selected={homography.observation_id === selectedObservationId}
                />
              ))
            : null}
          {showProjectionDiagnostics
            ? activeProjectionDiagnostics.map((diagnostic) => (
                <ProjectionDiagnosticGroup
                  diagnostic={diagnostic}
                  key={diagnostic.observation_id}
                  onSelect={onSelectProjectionDiagnostic}
                  overlaySize={overlaySize}
                  replayInfo={replayInfo}
                  selected={diagnostic.observation_id === selectedObservationId}
                />
              ))
            : null}
          {showCourtLines
            ? activeLines.map((lineEvidence) => (
                <CourtLineGroup
                  key={lineEvidence.observation_id}
                  lineEvidence={lineEvidence}
                  onSelect={onSelectCourtLine}
                  overlaySize={overlaySize}
                  replayInfo={replayInfo}
                  selected={lineEvidence.observation_id === selectedObservationId}
                />
              ))
            : null}
          {showRawCourtKeypoints
            ? activeKeypoints.map((keypointEvidence) => (
                <RawTomV1CourtKeypointGroup
                  key={`${keypointEvidence.observation_id}:raw`}
                  keypointEvidence={keypointEvidence}
                  onSelect={onSelectCourtKeypoint}
                  overlaySize={overlaySize}
                  replayInfo={replayInfo}
                  selected={keypointEvidence.observation_id === selectedObservationId}
                />
              ))
            : null}
          {showCourtKeypoints
            ? activeKeypoints.map((keypointEvidence) => (
                <CourtKeypointGroup
                  key={keypointEvidence.observation_id}
                  keypointEvidence={keypointEvidence}
                  onSelect={onSelectCourtKeypoint}
                  overlaySize={overlaySize}
                  replayInfo={replayInfo}
                  selected={keypointEvidence.observation_id === selectedObservationId}
                />
              ))
            : null}
        </svg>
      ) : null}
      {showCameraView && activeCameraViews.length > 0 ? (
        <div className="replay-camera-view-stack">
          {activeCameraViews.map((cameraView) => (
            <button
              className={`replay-camera-view-badge${
                cameraView.observation_id === selectedObservationId ? " selected" : ""
              }`}
              key={cameraView.observation_id}
              onClick={(event) => {
                event.stopPropagation();
                onSelectCameraView(cameraView);
              }}
              type="button"
            >
              <strong>{cameraView.view_label}</strong>
              <span>
                {cameraView.camera_motion_hint ?? "unknown"} ·{" "}
                {formatConfidence(cameraView.view_confidence)}
              </span>
            </button>
          ))}
        </div>
      ) : null}
      {status !== null ? <div className="replay-overlay-status court">{status}</div> : null}
    </div>
  );
}

function RawTomV1CourtKeypointGroup({
  keypointEvidence,
  replayInfo,
  overlaySize,
  selected,
  onSelect
}: {
  keypointEvidence: ReplayCourtKeypointOverlay;
  replayInfo: ReplayInfo;
  overlaySize: OverlaySize;
  selected: boolean;
  onSelect: (item: ReplayCourtKeypointOverlay) => void;
}) {
  const points = (keypointEvidence.raw_tom_v1_keypoints ?? [])
    .map((keypoint) => {
      if (
        !keypoint.present ||
        typeof keypoint.image_x !== "number" ||
        typeof keypoint.image_y !== "number"
      ) {
        return null;
      }
      const scaled = imagePixelPointToOverlayPoint(
        keypoint.image_x,
        keypoint.image_y,
        replayInfo.width,
        replayInfo.height,
        overlaySize.width,
        overlaySize.height
      );
      return scaled === null ? null : { keypoint, ...scaled };
    })
    .filter(
      (
        point
      ): point is {
        keypoint: NonNullable<ReplayCourtKeypointOverlay["raw_tom_v1_keypoints"]>[number];
        x: number;
        y: number;
      } => point !== null
    );
  return (
    <g
      aria-label={`raw TOM v1 court keypoint evidence frame ${keypointEvidence.frame_number}`}
      className={`replay-raw-court-keypoint-group${selected ? " selected" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(keypointEvidence);
      }}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect(keypointEvidence);
        }
      }}
      role="button"
      tabIndex={0}
    >
      {points.map(({ keypoint, x, y }) => (
        <g
          className="replay-raw-court-keypoint"
          key={`${keypointEvidence.observation_id}:raw:${keypoint.source_index}`}
        >
          <circle cx={x} cy={y} r={selected ? 5 : 4} />
          <text x={x + 6} y={y + 14}>
            {keypoint.label}
          </text>
        </g>
      ))}
    </g>
  );
}

function CourtKeypointGroup({
  keypointEvidence,
  replayInfo,
  overlaySize,
  selected,
  onSelect
}: {
  keypointEvidence: ReplayCourtKeypointOverlay;
  replayInfo: ReplayInfo;
  overlaySize: OverlaySize;
  selected: boolean;
  onSelect: (item: ReplayCourtKeypointOverlay) => void;
}) {
  const points = keypointEvidence.keypoints
    .map((keypoint) => scaleCourtKeypoint(keypoint, replayInfo, overlaySize))
    .filter((point): point is { keypoint: ReplayCourtKeypoint; x: number; y: number } => point !== null);
  return (
    <g
      aria-label={`court keypoint evidence frame ${keypointEvidence.frame_number}`}
      className={`replay-court-keypoint-group${selected ? " selected" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(keypointEvidence);
      }}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect(keypointEvidence);
        }
      }}
      role="button"
      tabIndex={0}
    >
      {points.map(({ keypoint, x, y }) => (
        <g className="replay-court-keypoint" key={`${keypointEvidence.observation_id}:${keypoint.name}`}>
          <circle cx={x} cy={y} r={selected ? 5 : 4} />
          <text x={x + 6} y={y - 6}>
            {keypointLabel(keypoint.name)}
          </text>
        </g>
      ))}
    </g>
  );
}

function CourtLineGroup({
  lineEvidence,
  replayInfo,
  overlaySize,
  selected,
  onSelect
}: {
  lineEvidence: ReplayCourtLineOverlay;
  replayInfo: ReplayInfo;
  overlaySize: OverlaySize;
  selected: boolean;
  onSelect: (item: ReplayCourtLineOverlay) => void;
}) {
  return (
    <g
      aria-label={`court line evidence frame ${lineEvidence.frame_number}`}
      className={`replay-court-line-group${selected ? " selected" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(lineEvidence);
      }}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect(lineEvidence);
        }
      }}
      role="button"
      tabIndex={0}
    >
      {lineEvidence.line_segments.map((segment) => {
        if (
          typeof segment.x1 !== "number" ||
          typeof segment.y1 !== "number" ||
          typeof segment.x2 !== "number" ||
          typeof segment.y2 !== "number"
        ) {
          return null;
        }
        const start = imagePixelPointToOverlayPoint(
          segment.x1,
          segment.y1,
          replayInfo.width,
          replayInfo.height,
          overlaySize.width,
          overlaySize.height
        );
        const end = imagePixelPointToOverlayPoint(
          segment.x2,
          segment.y2,
          replayInfo.width,
          replayInfo.height,
          overlaySize.width,
          overlaySize.height
        );
        if (start === null || end === null) {
          return null;
        }
        return (
          <line
            className="replay-court-line"
            key={`${lineEvidence.observation_id}:${segment.line_class}`}
            x1={start.x}
            x2={end.x}
            y1={start.y}
            y2={end.y}
          />
        );
      })}
    </g>
  );
}

function HomographyCandidateGroup({
  homography,
  replayInfo,
  overlaySize,
  selected,
  onSelect
}: {
  homography: ReplayHomographyCandidateOverlay;
  replayInfo: ReplayInfo;
  overlaySize: OverlaySize;
  selected: boolean;
  onSelect: (item: ReplayHomographyCandidateOverlay) => void;
}) {
  const template = homography.template ?? fallbackTemplate;
  const matrix = displayProjectionMatrix(homography);
  const templatePoints = new Map(
    template.keypoints
      .map((keypoint) => {
        const projected = projectTemplatePointWithMatrix(matrix, keypoint.x, keypoint.y);
        if (projected === null) {
          return null;
        }
        const scaled = imagePixelPointToOverlayPoint(
          projected.x,
          projected.y,
          replayInfo.width,
          replayInfo.height,
          overlaySize.width,
          overlaySize.height
        );
        return scaled === null ? null : [keypoint.name, scaled] as const;
      })
      .filter((entry): entry is readonly [string, { x: number; y: number }] => entry !== null)
  );
  return (
    <g
      aria-label={`homography candidate frame ${homography.frame_number}`}
      className={`replay-homography-group${selected ? " selected" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(homography);
      }}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect(homography);
        }
      }}
      role="button"
      tabIndex={0}
    >
      {template.lines.map((line) => {
        const start = templatePoints.get(line.start_keypoint);
        const end = templatePoints.get(line.end_keypoint);
        if (start === undefined || end === undefined) {
          return null;
        }
        return (
          <line
            className="replay-homography-line"
            key={`${homography.observation_id}:${line.line_class}`}
            x1={start.x}
            x2={end.x}
            y1={start.y}
            y2={end.y}
          />
        );
      })}
      {Array.from(templatePoints.entries()).map(([name, point]) => (
        <circle
          className="replay-homography-keypoint"
          cx={point.x}
          cy={point.y}
          key={`${homography.observation_id}:${name}`}
          r={selected ? 4 : 3}
        />
      ))}
    </g>
  );
}

function ProjectionDiagnosticGroup({
  diagnostic,
  replayInfo,
  overlaySize,
  selected,
  onSelect
}: {
  diagnostic: ReplayProjectionDiagnosticOverlay;
  replayInfo: ReplayInfo;
  overlaySize: OverlaySize;
  selected: boolean;
  onSelect: (item: ReplayProjectionDiagnosticOverlay) => void;
}) {
  const points = diagnostic.projected_template_keypoints
    .map((keypoint) => {
      if (!keypoint.valid || typeof keypoint.image_x !== "number" || typeof keypoint.image_y !== "number") {
        return null;
      }
      const scaled = imagePixelPointToOverlayPoint(
        keypoint.image_x,
        keypoint.image_y,
        replayInfo.width,
        replayInfo.height,
        overlaySize.width,
        overlaySize.height
      );
      return scaled === null ? null : [keypoint.name, scaled] as const;
    })
    .filter((entry): entry is readonly [string, { x: number; y: number }] => entry !== null);
  const pointsByName = new Map(points);
  return (
    <g
      aria-label={`projection diagnostic frame ${diagnostic.frame_number}`}
      className={`replay-projection-diagnostic-group${selected ? " selected" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(diagnostic);
      }}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect(diagnostic);
        }
      }}
      role="button"
      tabIndex={0}
    >
      {diagnostic.projected_template_lines.map((line) => {
        const start = pointsByName.get(line.start_keypoint);
        const end = pointsByName.get(line.end_keypoint);
        if (start === undefined || end === undefined) {
          return null;
        }
        return (
          <line
            className="replay-projection-diagnostic-line"
            key={`${diagnostic.observation_id}:${line.line_class}`}
            x1={start.x}
            x2={end.x}
            y1={start.y}
            y2={end.y}
          />
        );
      })}
      {points.map(([name, point]) => (
        <circle
          className="replay-projection-diagnostic-keypoint"
          cx={point.x}
          cy={point.y}
          key={`${diagnostic.observation_id}:${name}`}
          r={selected ? 4 : 3}
        />
      ))}
    </g>
  );
}

function scaleCourtKeypoint(
  keypoint: ReplayCourtKeypoint,
  replayInfo: ReplayInfo,
  overlaySize: OverlaySize
): { keypoint: ReplayCourtKeypoint; x: number; y: number } | null {
  if (!keypoint.present || typeof keypoint.x !== "number" || typeof keypoint.y !== "number") {
    return null;
  }
  const point = imagePixelPointToOverlayPoint(
    keypoint.x,
    keypoint.y,
    replayInfo.width,
    replayInfo.height,
    overlaySize.width,
    overlaySize.height
  );
  return point === null ? null : { keypoint, ...point };
}

function displayProjectionMatrix(
  homography: ReplayHomographyCandidateOverlay
): HomographyMatrix3x3 | null {
  if (
    homography.matrix_direction === "image_pixels_to_court_template_2d" &&
    homography.inverse_homography_matrix !== null
  ) {
    return homography.inverse_homography_matrix;
  }
  return homography.homography_matrix;
}

function keypointLabel(name: string): string {
  return name
    .replace("baseline_corner", "")
    .replace("service_line_t_", "t ")
    .replaceAll("_", " ")
    .trim();
}

function overlayStatus({
  enabled,
  isLoading,
  error,
  activeCount,
  totalCount
}: {
  enabled: boolean;
  isLoading: boolean;
  error: string | null;
  activeCount: number;
  totalCount: number;
}): string | null {
  if (!enabled) {
    return "Court evidence layers hidden.";
  }
  if (error !== null) {
    return error;
  }
  if (isLoading) {
    return "Loading court evidence overlays...";
  }
  if (totalCount === 0) {
    return "No court evidence in this time window.";
  }
  if (activeCount === 0) {
    return "No court evidence active at the current timestamp.";
  }
  return null;
}
