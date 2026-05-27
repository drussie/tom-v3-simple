"use client";

import { useMemo, useState } from "react";

import { getApiBaseUrl } from "../lib/api";
import { createAnnotation } from "../lib/api";
import {
  buildTrackletEvidenceModel,
  jsonRecordValue,
  stringValue
} from "../lib/trackletEvidence";
import type { HumanAnnotation, Tracklet, TrackletEvidenceBundle } from "../lib/types";
import type { TrackletEvidencePoint } from "../lib/types";
import { formatConfidence, formatFrameRange } from "../lib/timeline";

interface TrackletEvidencePanelProps {
  bundle: TrackletEvidenceBundle | null;
  error: string | null;
  isLoading: boolean;
  onAnnotationCreated: () => void;
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
  onAnnotationCreated,
  onSelectObservation,
  onSelectTracklet,
  selectedObservationId,
  selectedTrackletId,
  tracklets
}: TrackletEvidencePanelProps) {
  if (tracklets.length === 0) {
    return (
      <section className="panel tracklet-evidence-panel">
        <div className="panel-header">
          <h2>Tracklet Candidate Evidence</h2>
          <span className="mini-pill">0 tracklet candidates</span>
        </div>
        <div className="panel-body tracklet-evidence-body">
          <p className="empty-state">
            No candidate tracklets found for this run. Run `build-tracklets` with a detection run id
            or run `make demo` to create fixture tracklet evidence.
          </p>
        </div>
      </section>
    );
  }

  const model = buildTrackletEvidenceModel(bundle, selectedObservationId);
  const reviewTargets = useMemo(
    () => buildReviewTargets(bundle, model?.selectedPoint ?? null),
    [bundle, model?.selectedPoint]
  );

  return (
    <section className="panel tracklet-evidence-panel">
      <div className="panel-header">
        <h2>Tracklet Candidate Evidence</h2>
        <span className="mini-pill">{tracklets.length} tracklet candidates</span>
      </div>
      <div className="panel-body tracklet-evidence-body">
        <TrackletSelector
          bundle={bundle}
          onSelectTracklet={onSelectTracklet}
          selectedTrackletId={selectedTrackletId}
          tracklets={tracklets}
        />

        {isLoading ? <p className="empty-state">Loading evidence bundle...</p> : null}
        {error ? <p className="empty-state">{error}</p> : null}

        {bundle && model ? (
          <>
            <p className="evidence-note">
              Candidate temporal grouping. This does not decide object identity or ball path
              correctness.
            </p>
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
            <ReviewAnnotationHistory bundle={bundle} point={model.selectedPoint} />
            <TrackletReviewForm
              mediaId={bundle.media?.id ?? bundle.tracklet.typed.media_id}
              onAnnotationCreated={onAnnotationCreated}
              targets={reviewTargets}
            />
          </>
        ) : null}
        {!isLoading && !error && (!bundle || !model) ? (
          <p className="empty-state">
            No tracklet evidence bundle loaded. Select a tracklet candidate to inspect source
            detections, track point candidates, lineage, and review annotations.
          </p>
        ) : null}
      </div>
    </section>
  );
}

function TrackletSelector({
  bundle,
  onSelectTracklet,
  selectedTrackletId,
  tracklets
}: {
  bundle: TrackletEvidenceBundle | null;
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
          {tracklet.id === selectedTrackletId && bundle ? (
            <span>{bundle.tracklet.annotation_summary.count} review annotations</span>
          ) : null}
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
          <span>
            {point.source_detection?.observation_type
              ? "source detection observation"
              : "source n/a"}
          </span>
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
          <h3>Selected Source Detection Observation</h3>
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
        <SummaryCell
          label="Source detection observation"
          value={point.source_detection_observation_id ?? "n/a"}
        />
        <SummaryCell label="Track point candidate obs" value={point.observation?.id ?? "n/a"} />
        <SummaryCell label="tracked_from lineage" value={point.lineage_to_source?.id ?? "missing"} />
        <SummaryCell
          label="grouped_from lineage"
          value={point.lineage_to_tracklet?.id ?? "missing"}
        />
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

interface ReviewTarget {
  kind: "tracklet_candidate" | "track_point_candidate" | "source_detection";
  label: string;
  observationId: string;
}

const REVIEW_LABELS = [
  "likely_good_tracklet",
  "bad_tracklet",
  "identity_switch",
  "wrong_grouping",
  "fragmented_tracklet",
  "merged_multiple_objects",
  "uncertain",
  "wrong_point_assignment",
  "point_should_start_new_tracklet",
  "point_should_belong_to_previous_tracklet",
  "bad_source_detection",
  "wrong_class_label",
  "bad_bbox",
  "duplicate_detection",
  "missed_ball_nearby"
];

function buildReviewTargets(
  bundle: TrackletEvidenceBundle | null,
  point: TrackletEvidencePoint | null
): ReviewTarget[] {
  if (!bundle) {
    return [];
  }
  const targets: ReviewTarget[] = [];
  if (bundle.tracklet.observation) {
    targets.push({
      kind: "tracklet_candidate",
      label: "selected tracklet candidate",
      observationId: bundle.tracklet.observation.id
    });
  }
  if (point?.observation) {
    targets.push({
      kind: "track_point_candidate",
      label: `track point candidate frame ${point.frame_number}`,
      observationId: point.observation.id
    });
  }
  if (point?.source_detection) {
    targets.push({
      kind: "source_detection",
      label: `source detection frame ${point.frame_number}`,
      observationId: point.source_detection.id
    });
  }
  return targets;
}

function ReviewAnnotationHistory({
  bundle,
  point
}: {
  bundle: TrackletEvidenceBundle;
  point: TrackletEvidencePoint | null;
}) {
  const sourceAnnotations =
    point?.source_detection !== null && point?.source_detection !== undefined
      ? bundle.source_detections.find((row) => row.observation.id === point.source_detection?.id)
          ?.annotations ?? []
      : [];

  return (
    <div className="review-history">
      <h3>Review Annotations</h3>
      <AnnotationGroup
        annotations={bundle.tracklet.annotations}
        label="Tracklet candidate annotations"
      />
      <AnnotationGroup
        annotations={point?.annotations ?? []}
        label="Track point candidate annotations"
      />
      <AnnotationGroup
        annotations={sourceAnnotations}
        label="Source detection annotations"
      />
    </div>
  );
}

function AnnotationGroup({
  annotations,
  label
}: {
  annotations: HumanAnnotation[];
  label: string;
}) {
  return (
    <div className="review-annotation-group">
      <strong>{label}</strong>
      {annotations.length === 0 ? <span className="empty-state">none</span> : null}
      {annotations.map((annotation) => (
        <div className="annotation-row" key={annotation.id}>
          <strong>{annotation.annotation_type}</strong>
          <span className="mono">{annotation.created_by ?? "local reviewer"}</span>
          {typeof annotation.payload_jsonb.notes === "string" ? (
            <p>{annotation.payload_jsonb.notes}</p>
          ) : null}
        </div>
      ))}
    </div>
  );
}

function TrackletReviewForm({
  mediaId,
  onAnnotationCreated,
  targets
}: {
  mediaId: string;
  onAnnotationCreated: () => void;
  targets: ReviewTarget[];
}) {
  const [targetId, setTargetId] = useState(targets[0]?.observationId ?? "");
  const [label, setLabel] = useState(REVIEW_LABELS[0]);
  const [notes, setNotes] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const selectedTarget = targets.find((target) => target.observationId === targetId) ?? targets[0];

  if (targets.length === 0 || selectedTarget === undefined) {
    return <p className="empty-state">No review target is available for this evidence bundle.</p>;
  }

  return (
    <form
      className="tracklet-review-form"
      onSubmit={(event) => {
        event.preventDefault();
        setStatus("Saving review annotation...");
        createAnnotation({
          media_id: mediaId,
          observation_id: selectedTarget.observationId,
          annotation_type: label,
          payload_jsonb: {
            annotation_label: label,
            notes,
            review_context: "tracklet_evidence_bundle",
            review_status: "reviewed",
            target_kind: selectedTarget.kind,
            created_from_view: "tracklet_evidence_panel"
          },
          created_by: "local-reviewer"
        })
          .then(() => {
            setNotes("");
            setStatus("Review annotation saved.");
            onAnnotationCreated();
          })
          .catch((error: unknown) => {
            setStatus(error instanceof Error ? error.message : "Unable to save annotation.");
          });
      }}
    >
      <h3>Tracklet Review</h3>
      <label>
        Target
        <select value={selectedTarget.observationId} onChange={(event) => setTargetId(event.target.value)}>
          {targets.map((target) => (
            <option key={target.observationId} value={target.observationId}>
              {target.label}
            </option>
          ))}
        </select>
      </label>
      <label>
        Review label
        <select value={label} onChange={(event) => setLabel(event.target.value)}>
          {REVIEW_LABELS.map((reviewLabel) => (
            <option key={reviewLabel} value={reviewLabel}>
              {reviewLabel}
            </option>
          ))}
        </select>
      </label>
      <label>
        Notes
        <textarea
          onChange={(event) => setNotes(event.target.value)}
          placeholder="Optional review note"
          rows={3}
          value={notes}
        />
      </label>
      <button className="quiet-button" type="submit">
        Add review annotation
      </button>
      {status ? <p className="empty-state">{status}</p> : null}
    </form>
  );
}
