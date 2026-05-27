import { useState } from "react";

import { PoseOverlayCanvas } from "./PoseOverlayCanvas";
import type { PoseOverlayItem, PoseOverlayModel } from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface PoseOverlayPanelProps {
  model: PoseOverlayModel;
  onSelectObservation: (observationId: string) => void;
}

export function PoseOverlayPanel({ model, onSelectObservation }: PoseOverlayPanelProps) {
  const [showPoseObservations, setShowPoseObservations] = useState(true);
  const [showSkeletonEdges, setShowSkeletonEdges] = useState(true);
  const [showKeypointLabels, setShowKeypointLabels] = useState(false);
  const [showLowConfidenceKeypoints, setShowLowConfidenceKeypoints] = useState(true);
  const mediaWidth = model.mediaWidth;
  const mediaHeight = model.mediaHeight;
  const selectedFrame = model.selectedFrame;
  const canRender =
    model.unavailableReason === null &&
    mediaWidth !== null &&
    mediaHeight !== null &&
    selectedFrame !== null;

  return (
    <section className="panel pose-overlay-panel">
      <div className="panel-header">
        <h2>Pose Overlay</h2>
        <span className="mini-pill">frame {selectedFrame ?? "n/a"}</span>
      </div>
      <div className="panel-body pose-overlay-body">
        <div className="overlay-summary">
          <span>{model.items.length} pose observations</span>
          <span>{model.frameItems.length} on selected frame</span>
          <span>COCO17 keypoint evidence</span>
        </div>
        <p className="evidence-note">
          Pose observations are keypoint evidence only. They do not classify strokes, movement, or
          biomechanics.
        </p>

        <div className="pose-toggle-grid" aria-label="Pose overlay controls">
          <label>
            <input
              checked={showPoseObservations}
              onChange={(event) => setShowPoseObservations(event.target.checked)}
              type="checkbox"
            />
            Show pose observations
          </label>
          <label>
            <input
              checked={showSkeletonEdges}
              onChange={(event) => setShowSkeletonEdges(event.target.checked)}
              type="checkbox"
            />
            Show skeleton edges
          </label>
          <label>
            <input
              checked={showKeypointLabels}
              onChange={(event) => setShowKeypointLabels(event.target.checked)}
              type="checkbox"
            />
            Show keypoint labels
          </label>
          <label>
            <input
              checked={showLowConfidenceKeypoints}
              onChange={(event) => setShowLowConfidenceKeypoints(event.target.checked)}
              type="checkbox"
            />
            Show low-confidence keypoints
          </label>
        </div>

        {canRender && showPoseObservations ? (
          <PoseOverlayCanvas
            items={model.frameItems}
            mediaHeight={mediaHeight}
            mediaWidth={mediaWidth}
            onSelectObservation={onSelectObservation}
            selectedFrame={selectedFrame}
            showKeypointLabels={showKeypointLabels}
            showLowConfidenceKeypoints={showLowConfidenceKeypoints}
            showSkeletonEdges={showSkeletonEdges}
          />
        ) : (
          <p className="empty-state">
            {showPoseObservations
              ? model.unavailableReason ??
                "No pose overlay available for this frame. Run run-pose-adapter or make demo to generate fixture pose evidence."
              : "Pose overlay hidden; persisted pose evidence remains listed below."}
          </p>
        )}

        <p className="frame-artifact-state">
          Pose markers use persisted full-frame image-pixel coordinates. Missing keypoints stay in
          the table and are not drawn as present markers.
        </p>

        <PoseFrameList items={model.frameItems} onSelectObservation={onSelectObservation} />
        <SelectedPoseDetail item={model.selectedPoseItem} />
      </div>
    </section>
  );
}

function PoseFrameList({
  items,
  onSelectObservation
}: {
  items: PoseOverlayModel["frameItems"];
  onSelectObservation: (observationId: string) => void;
}) {
  if (items.length === 0) {
    return (
      <p className="empty-state">
        No pose observations found for this frame. Run `run-pose-adapter` or `make demo` to generate
        fixture pose evidence.
      </p>
    );
  }

  return (
    <div className="pose-frame-list">
      {items.map((item) => (
        <button
          className={`pose-frame-row${item.isSelected ? " selected" : ""}`}
          key={item.id}
          onClick={() => onSelectObservation(item.observationId)}
          type="button"
        >
          <strong>{item.skeletonFormat}/{item.skeletonVersion}</strong>
          <span>{item.keypointsPresentCount} present keypoints</span>
          <span>{formatConfidence(item.poseConfidence)}</span>
        </button>
      ))}
    </div>
  );
}

function SelectedPoseDetail({ item }: { item: PoseOverlayItem | null }) {
  if (item === null) {
    return <p className="empty-state">Select a pose observation to inspect keypoint evidence.</p>;
  }

  return (
    <div className="pose-detail-stack">
      <div className="pose-detail-grid">
        <div>
          <strong>Pose observation</strong>
          <span className="mono">{item.observationId}</span>
        </div>
        <div>
          <strong>Skeleton</strong>
          <span>{item.skeletonFormat}/{item.skeletonVersion}</span>
        </div>
        <div>
          <strong>Pose confidence</strong>
          <span>{formatConfidence(item.poseConfidence)}</span>
        </div>
        <div>
          <strong>Keypoints</strong>
          <span>
            {item.keypointsPresentCount} present / {item.keypointsMissingCount} missing
          </span>
        </div>
        <div>
          <strong>Mean keypoint confidence</strong>
          <span>{formatConfidence(item.meanKeypointConfidence)}</span>
        </div>
        <div>
          <strong>Frame time owner</strong>
          <span>{item.frameTimeOwner}</span>
        </div>
        <div>
          <strong>Bbox</strong>
          <span>{formatPoseBBox(item)}</span>
        </div>
        <div>
          <strong>Association</strong>
          <span>
            {item.associationStatus}
            {item.associationMethod !== null ? ` via ${item.associationMethod}` : ""}
          </span>
        </div>
      </div>
      <SourceContext item={item} />
      <KeypointTable item={item} />
    </div>
  );
}

function SourceContext({ item }: { item: PoseOverlayItem }) {
  const hasSource =
    item.subjectRefType !== "none" ||
    item.subjectDetectionObservationId !== null ||
    item.subjectTrackletId !== null ||
    item.subjectTrackPointId !== null;

  if (!hasSource) {
    return (
      <div className="source-context-card">
        <h3>Source Context</h3>
        <p>Unassociated full-frame pose observation.</p>
      </div>
    );
  }

  return (
    <div className="source-context-card">
      <h3>Source Context</h3>
      <dl className="key-value">
        <dt>Subject ref</dt>
        <dd>{item.subjectRefType}</dd>
        <dt>Status</dt>
        <dd>{item.associationStatus}</dd>
        <dt>Method</dt>
        <dd>{item.associationMethod ?? "n/a"}</dd>
        <dt>Confidence</dt>
        <dd>{formatConfidence(item.associationConfidence)}</dd>
        <dt>Source detection</dt>
        <dd className="mono">{item.subjectDetectionObservationId ?? "n/a"}</dd>
        <dt>Tracklet candidate</dt>
        <dd className="mono">{item.subjectTrackletId ?? "n/a"}</dd>
        <dt>Track point candidate</dt>
        <dd className="mono">{item.subjectTrackPointId ?? "n/a"}</dd>
      </dl>
    </div>
  );
}

function KeypointTable({ item }: { item: PoseOverlayItem }) {
  return (
    <div className="keypoint-table-wrap">
      <h3>Keypoint Evidence</h3>
      <table className="keypoint-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>X</th>
            <th>Y</th>
            <th>Confidence</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {item.keypoints.map((keypoint) => (
            <tr key={keypoint.index}>
              <td>{keypoint.name}</td>
              <td>{formatNumber(keypoint.x)}</td>
              <td>{formatNumber(keypoint.y)}</td>
              <td>{formatConfidence(keypoint.confidence)}</td>
              <td>{keypoint.present ? "present" : "missing"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatPoseBBox(item: PoseOverlayItem): string {
  if (item.bbox === null) {
    return "n/a";
  }
  return `${formatNumber(item.bbox.x)}, ${formatNumber(item.bbox.y)}, ${formatNumber(
    item.bbox.width
  )} x ${formatNumber(item.bbox.height)}`;
}

function formatNumber(value: number | null): string {
  if (value === null || !Number.isFinite(value)) {
    return "n/a";
  }
  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}
