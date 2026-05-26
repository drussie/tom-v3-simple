import type { PoseOverlayItem, PoseOverlayKeypoint } from "../lib/types";

interface PoseOverlayCanvasProps {
  items: PoseOverlayItem[];
  mediaWidth: number;
  mediaHeight: number;
  selectedFrame: number;
  showSkeletonEdges: boolean;
  showKeypointLabels: boolean;
  showLowConfidenceKeypoints: boolean;
  onSelectObservation: (observationId: string) => void;
}

export function PoseOverlayCanvas({
  items,
  mediaWidth,
  mediaHeight,
  selectedFrame,
  showSkeletonEdges,
  showKeypointLabels,
  showLowConfidenceKeypoints,
  onSelectObservation
}: PoseOverlayCanvasProps) {
  return (
    <div
      aria-label={`Pose overlay frame ${selectedFrame}`}
      className="detection-canvas pose-canvas"
      style={{ aspectRatio: `${mediaWidth} / ${mediaHeight}` }}
    >
      <div className="detection-canvas-grid" />
      <div className="frame-space-label">
        <strong>image_pixels</strong>
        <span>
          {mediaWidth} x {mediaHeight}
        </span>
      </div>
      <svg
        aria-hidden="true"
        className="pose-svg-layer"
        preserveAspectRatio="none"
        viewBox={`0 0 ${mediaWidth} ${mediaHeight}`}
      >
        {items.map((item) => (
          <g
            className={`pose-group${item.isSelected ? " selected" : ""}`}
            key={item.id}
            onClick={() => onSelectObservation(item.observationId)}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                onSelectObservation(item.observationId);
              }
            }}
            role="button"
            tabIndex={0}
          >
            {item.bbox !== null ? (
              <rect
                className="pose-bbox"
                height={item.bbox.height}
                vectorEffect="non-scaling-stroke"
                width={item.bbox.width}
                x={item.bbox.x}
                y={item.bbox.y}
              />
            ) : null}
            {showSkeletonEdges
              ? item.edges.map((edge) => (
                  <line
                    className="pose-edge"
                    key={edge.id}
                    vectorEffect="non-scaling-stroke"
                    x1={edge.start.x ?? 0}
                    x2={edge.end.x ?? 0}
                    y1={edge.start.y ?? 0}
                    y2={edge.end.y ?? 0}
                  />
                ))
              : null}
            {visibleKeypoints(item.presentKeypoints, showLowConfidenceKeypoints).map(
              (keypoint) => (
                <g className="pose-keypoint-wrap" key={keypoint.name}>
                  <circle
                    className={`pose-keypoint ${keypoint.confidenceBand}`}
                    cx={keypoint.x ?? 0}
                    cy={keypoint.y ?? 0}
                    r={5}
                    vectorEffect="non-scaling-stroke"
                  />
                  {showKeypointLabels ? (
                    <text
                      className="pose-keypoint-label"
                      dominantBaseline="middle"
                      x={(keypoint.x ?? 0) + 8}
                      y={(keypoint.y ?? 0) - 8}
                    >
                      {keypoint.name}
                    </text>
                  ) : null}
                </g>
              )
            )}
          </g>
        ))}
      </svg>
    </div>
  );
}

function visibleKeypoints(
  keypoints: PoseOverlayKeypoint[],
  showLowConfidenceKeypoints: boolean
): PoseOverlayKeypoint[] {
  if (showLowConfidenceKeypoints) {
    return keypoints;
  }
  return keypoints.filter((keypoint) => keypoint.confidenceBand !== "low");
}
