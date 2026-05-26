import { getApiBaseUrl } from "../lib/api";
import {
  buildTrackletEvidenceModel,
  jsonRecordValue,
  stringValue
} from "../lib/trackletEvidence";
import type { Tracklet, TrackletEvidenceBundle } from "../lib/types";
import type { TrackletEvidencePoint } from "../lib/types";
import { formatConfidence, formatFrameRange } from "../lib/timeline";

interface TrackletEvidencePanelProps {
  bundle: TrackletEvidenceBundle | null;
  error: string | null;
  isLoading: boolean;
  onSelectObservation: (observationId: string) => void;
  onSelectTracklet: (tracklet: Tracklet) => void;
  selectedObservationId: string | null;
  selectedTrackletId: string | null;
  tracklets: Tracklet[];
}

export function TrackletEvidencePanel({
  bundle,
  error,
  isLoading,
  onSelectObservation,
  onSelectTracklet,
  selectedObservationId,
  selectedTrackletId,
  tracklets
}: TrackletEvidencePanelProps) {
  if (tracklets.length === 0) {
    return null;
  }

  const model = buildTrackletEvidenceModel(bundle, selectedObservationId);

  return (
    <section className="panel tracklet-evidence-panel">
      <div className="panel-header">
        <h2>Tracklet Evidence</h2>
        <span className="mini-pill">{tracklets.length} tracklet candidates</span>
      </div>
      <div className="panel-body tracklet-evidence-body">
        <TrackletSelector
          onSelectTracklet={onSelectTracklet}
          selectedTrackletId={selectedTrackletId}
          tracklets={tracklets}
        />

        {isLoading ? <p className="empty-state">Loading evidence bundle...</p> : null}
        {error ? <p className="empty-state">{error}</p> : null}

        {bundle && model ? (
          <>
            <div className="tracklet-summary-grid">
              <SummaryCell label="Status" value={model.status} />
              <SummaryCell label="Identity" value={model.identityStatus} />
              <SummaryCell label="Frame range" value={model.frameRange} />
              <SummaryCell label="Confidence" value={formatConfidence(bundle.summary.confidence)} />
              <SummaryCell label="Track points" value={String(bundle.summary.track_point_count)} />
              <SummaryCell
                label="Source detections"
                value={String(bundle.summary.source_detection_count)}
              />
              <SummaryCell label="Source run" value={model.sourceRunId ?? "n/a"} />
              <SummaryCell label="Tracklet obs" value={bundle.tracklet.observation?.id ?? "n/a"} />
            </div>
            <p className="evidence-warning">{model.warning}</p>
            <TrackPointList
              bundle={bundle}
              onSelectObservation={onSelectObservation}
              selectedObservationId={selectedObservationId}
            />
            <SelectedTrackPointEvidence
              bundle={bundle}
              point={model.selectedPoint}
              onSelectObservation={onSelectObservation}
            />
          </>
        ) : null}
      </div>
    </section>
  );
}

function TrackletSelector({
  onSelectTracklet,
  selectedTrackletId,
  tracklets
}: {
  onSelectTracklet: (tracklet: Tracklet) => void;
  selectedTrackletId: string | null;
  tracklets: Tracklet[];
}) {
  return (
    <div className="tracklet-selector">
      {tracklets.map((tracklet) => (
        <button
          className={`tracklet-selector-row${tracklet.id === selectedTrackletId ? " selected" : ""}`}
          key={tracklet.id}
          onClick={() => onSelectTracklet(tracklet)}
          type="button"
        >
          <strong>{tracklet.subject_ref ?? tracklet.track_family} candidate</strong>
          <span>{formatFrameRange(tracklet.frame_start, tracklet.frame_end)}</span>
          <span>{formatConfidence(tracklet.confidence)}</span>
        </button>
      ))}
    </div>
  );
}

function SummaryCell({ label, value }: { label: string; value: string }) {
  return (
    <div className="media-cell">
      <strong>{label}</strong>
      <span>{value}</span>
    </div>
  );
}

function TrackPointList({
  bundle,
  onSelectObservation,
  selectedObservationId
}: {
  bundle: TrackletEvidenceBundle;
  onSelectObservation: (observationId: string) => void;
  selectedObservationId: string | null;
}) {
  return (
    <div className="track-point-list">
      <h3>Track Point Candidates</h3>
      {bundle.track_points.map((point) => (
        <button
          className={`track-point-row${
            point.observation?.id === selectedObservationId ? " selected" : ""
          }`}
          disabled={point.observation === null}
          key={point.typed.id}
          onClick={() => {
            if (point.observation) {
              onSelectObservation(point.observation.id);
            }
          }}
          type="button"
        >
          <span>#{point.sequence_index ?? "n/a"}</span>
          <strong>frame {point.frame_number}</strong>
          <span>{formatConfidence(point.typed.confidence)}</span>
          <span>{point.source_detection?.observation_type ?? "source n/a"}</span>
        </button>
      ))}
    </div>
  );
}

function SelectedTrackPointEvidence({
  bundle,
  onSelectObservation,
  point
}: {
  bundle: TrackletEvidenceBundle;
  onSelectObservation: (observationId: string) => void;
  point: TrackletEvidencePoint | null;
}) {
  if (point === null) {
    return <p className="empty-state">No track point candidate selected.</p>;
  }

  const sourcePayload = point.source_detection?.payload_jsonb ?? {};
  const atomicPayload = point.source_detection?.atomic?.payload_jsonb ?? {};
  const bbox = jsonRecordValue(point.bbox ?? sourcePayload.bbox ?? atomicPayload.bbox);
  const label = stringValue(
    point.source_detection?.payload_jsonb.label ??
      point.source_detection?.atomic?.payload_jsonb.label ??
      point.source_detection?.payload_jsonb.class_label ??
      point.source_detection?.atomic?.payload_jsonb.class_label,
    point.source_detection?.observation_type ?? "source detection"
  );
  const artifact = point.frame_artifacts[0] ?? null;
  const artifactUrl = artifact ? `${getApiBaseUrl()}/artifacts/${artifact.id}/content` : null;

  return (
    <div className="source-detection-card">
      <div className="source-detection-header">
        <div>
          <h3>Selected Source Detection</h3>
          <p>
            {label} / {point.source_detection?.observation_type ?? "n/a"} / frame{" "}
            {point.frame_number}
          </p>
        </div>
        {point.source_detection ? (
          <button
            className="text-button"
            onClick={() => onSelectObservation(point.source_detection!.id)}
            type="button"
          >
            Select source
          </button>
        ) : null}
      </div>

      {artifactUrl ? (
        <div className="tracklet-frame-preview">
          <img alt="Frame artifact for source detection" src={artifactUrl} />
        </div>
      ) : (
        <p className="empty-state">
          No frame image artifact is available for this source detection; showing bbox metadata.
        </p>
      )}

      <div className="tracklet-summary-grid">
        <SummaryCell label="Source obs" value={point.source_detection_observation_id ?? "n/a"} />
        <SummaryCell label="Point obs" value={point.observation?.id ?? "n/a"} />
        <SummaryCell label="tracked_from" value={point.lineage_to_source?.id ?? "missing"} />
        <SummaryCell label="grouped_from" value={point.lineage_to_tracklet?.id ?? "missing"} />
        <SummaryCell label="bbox x/y" value={`${bbox.x ?? "n/a"} / ${bbox.y ?? "n/a"}`} />
        <SummaryCell
          label="bbox w/h"
          value={`${bbox.width ?? "n/a"} / ${bbox.height ?? "n/a"}`}
        />
      </div>

      <details className="json-details">
        <summary>Bundle lineage rows ({bundle.lineage.length})</summary>
        <pre>{JSON.stringify(bundle.lineage, null, 2)}</pre>
      </details>
    </div>
  );
}
