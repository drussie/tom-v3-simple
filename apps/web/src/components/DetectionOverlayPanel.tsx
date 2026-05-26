import { DetectionLegend } from "./DetectionLegend";
import { DetectionOverlayCanvas } from "./DetectionOverlayCanvas";
import { getApiBaseUrl } from "../lib/api";
import type { DetectionOverlayModel } from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface DetectionOverlayPanelProps {
  model: DetectionOverlayModel;
  onSelectObservation: (observationId: string) => void;
}

export function DetectionOverlayPanel({
  model,
  onSelectObservation
}: DetectionOverlayPanelProps) {
  const mediaWidth = model.mediaWidth;
  const mediaHeight = model.mediaHeight;
  const selectedFrame = model.selectedFrame;
  const frameArtifactUrl =
    model.frameArtifact === null
      ? null
      : `${getApiBaseUrl()}/artifacts/${model.frameArtifact.artifact.id}/content`;
  const canRender =
    model.unavailableReason === null &&
    mediaWidth !== null &&
    mediaHeight !== null &&
    selectedFrame !== null;

  return (
    <section className="panel detection-overlay-panel">
      <div className="panel-header">
        <h2>Detection Overlay</h2>
        <span className="mini-pill">frame {model.selectedFrame ?? "n/a"}</span>
      </div>
      <div className="panel-body detection-overlay-body">
        <div className="overlay-summary">
          <span>{model.items.length} detections with bboxes</span>
          <span>{model.frameItems.length} on selected frame</span>
          {model.missingBboxObservationIds.length > 0 ? (
            <span>{model.missingBboxObservationIds.length} missing bbox payload</span>
          ) : null}
        </div>

        {canRender ? (
          <DetectionOverlayCanvas
            frameImageUrl={frameArtifactUrl}
            items={model.frameItems}
            mediaHeight={mediaHeight}
            mediaWidth={mediaWidth}
            onSelectObservation={onSelectObservation}
            selectedFrame={selectedFrame}
          />
        ) : (
          <p className="empty-state">{model.unavailableReason}</p>
        )}

        {canRender ? (
          <p className="frame-artifact-state">
            {model.frameArtifact === null
              ? "No frame image artifact is available for this frame; showing image_pixels coordinate canvas."
              : `Showing ${model.frameArtifact.artifact.artifact_type} artifact for ${
                  model.frameArtifact.match === "selected_observation"
                    ? "selected observation"
                    : "selected frame"
                }.`}
          </p>
        ) : null}

        <DetectionLegend />
        <DetectionFrameList items={model.frameItems} onSelectObservation={onSelectObservation} />
      </div>
    </section>
  );
}

function DetectionFrameList({
  items,
  onSelectObservation
}: {
  items: DetectionOverlayModel["frameItems"];
  onSelectObservation: (observationId: string) => void;
}) {
  if (items.length === 0) {
    return <p className="empty-state">No bbox observations on this frame.</p>;
  }

  return (
    <div className="detection-frame-list">
      {items.map((item) => (
        <button
          className={`detection-frame-row${item.isSelected ? " selected" : ""}`}
          key={item.id}
          onClick={() => onSelectObservation(item.observationId)}
          type="button"
        >
          <strong>{item.label}</strong>
          <span>{item.observationType}</span>
          <span>{formatConfidence(item.confidence)}</span>
        </button>
      ))}
    </div>
  );
}
