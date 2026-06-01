"use client";

import { useEffect, useState } from "react";

import type {
  EventCandidateReviewAnnotation,
  EventCandidateReviewLabel,
  ReplayMarkerSummary
} from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayMarkerInspectorProps {
  selectedMarker: ReplayMarkerSummary | null;
  markerCount: number;
  eventCandidateRunId: string | null;
  reviews: EventCandidateReviewAnnotation[];
  reviewSaving: boolean;
  reviewError: string | null;
  onDeleteReview: (reviewId: string) => Promise<void>;
  onSaveReview: (
    reviewLabel: EventCandidateReviewLabel,
    note: string,
    reviewId: string | null
  ) => Promise<void>;
}

export function ReplayMarkerInspector({
  selectedMarker,
  markerCount,
  eventCandidateRunId,
  reviews,
  reviewSaving,
  reviewError,
  onDeleteReview,
  onSaveReview
}: ReplayMarkerInspectorProps) {
  if (selectedMarker === null) {
    return (
      <section className="panel replay-marker-inspector">
        <div className="panel-header">
          <h2>Marker Inspector</h2>
          <span className="mini-pill">{markerCount} markers</span>
        </div>
        <div className="panel-body">
          <p className="empty-state compact">
            No marker selected. Click a hit or bounce marker to inspect candidate evidence.
          </p>
          <p className="marker-inspector-warning">
            Candidate evidence only - not truth, not score, not in/out.
          </p>
        </div>
      </section>
    );
  }

  const isHit = selectedMarker.candidate_type === "hit_candidate";
  const markerLabel = isHit ? "HIT CANDIDATE" : "BOUNCE CANDIDATE";
  const sourceMethod =
    selectedMarker.source_method ??
    selectedMarker.original_candidate_method ??
    selectedMarker.candidate_method ??
    "n/a";
  const latestReview = latestCandidateMarkerReview(reviews);

  return (
    <section className={`panel replay-marker-inspector ${isHit ? "hit" : "bounce"}`}>
      <div className="panel-header">
        <h2>Selected Marker</h2>
        <span className={`mini-pill marker-type-pill ${isHit ? "hit" : "bounce"}`}>
          {markerLabel}
        </span>
      </div>
      <div className="panel-body marker-inspector-body">
        <div className="marker-inspector-hero">
          <span className={`marker-inspector-icon ${isHit ? "hit" : "bounce"}`} />
          <div>
            <strong>{markerLabel}</strong>
            <span>frame {selectedMarker.frame} / {selectedMarker.timestamp_ms} ms</span>
          </div>
        </div>
        <div className="marker-inspector-grid">
          <MarkerInspectorRow label="source" value={sourceMethod} />
          <MarkerInspectorRow
            label="confidence"
            value={formatConfidence(selectedMarker.confidence ?? null)}
          />
          <MarkerInspectorRow
            label="decision"
            value={selectedMarker.arbitration_decision ?? "n/a"}
          />
          <MarkerInspectorRow
            label="reason"
            value={selectedMarker.arbitration_reason ?? "n/a"}
          />
          <MarkerInspectorRow
            label="image"
            value={formatCoordinates(selectedMarker.image_x, selectedMarker.image_y)}
          />
          <MarkerInspectorRow
            label="court"
            value={formatCoordinates(selectedMarker.court_x, selectedMarker.court_y)}
          />
        </div>
        {selectedMarker.original_candidate_type !== null &&
        selectedMarker.original_candidate_type !== undefined &&
        selectedMarker.original_candidate_type !== selectedMarker.candidate_type ? (
          <p className="marker-inspector-note">
            Original source type: {selectedMarker.original_candidate_type}. Final marker type:
            {" "}
            {selectedMarker.candidate_type}.
          </p>
        ) : null}
        <p className="marker-inspector-warning">
          Candidate evidence only - not truth, not score, not in/out.
        </p>
        <MarkerReviewControls
          eventCandidateRunId={eventCandidateRunId}
          latestReview={latestReview}
          onDeleteReview={onDeleteReview}
          onSaveReview={onSaveReview}
          reviewError={reviewError}
          reviewSaving={reviewSaving}
          selectedObservationId={selectedMarker.observation_id}
        />
      </div>
    </section>
  );
}

function MarkerInspectorRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="marker-inspector-row">
      <strong>{label}</strong>
      <span>{value}</span>
    </div>
  );
}

function formatCoordinates(x: number | null | undefined, y: number | null | undefined): string {
  if (x === null || y === null || x === undefined || y === undefined) {
    return "n/a";
  }
  return `x=${x.toFixed(3)}, y=${y.toFixed(3)}`;
}

const markerReviewLabels: Array<{
  label: EventCandidateReviewLabel;
  text: string;
}> = [
  { label: "useful", text: "Useful" },
  { label: "wrong", text: "Wrong" },
  { label: "unclear", text: "Unclear" },
  { label: "needs_review", text: "Needs review" }
];

function MarkerReviewControls({
  eventCandidateRunId,
  latestReview,
  onDeleteReview,
  onSaveReview,
  reviewError,
  reviewSaving,
  selectedObservationId
}: {
  eventCandidateRunId: string | null;
  latestReview: EventCandidateReviewAnnotation | null;
  onDeleteReview: (reviewId: string) => Promise<void>;
  onSaveReview: (
    reviewLabel: EventCandidateReviewLabel,
    note: string,
    reviewId: string | null
  ) => Promise<void>;
  reviewError: string | null;
  reviewSaving: boolean;
  selectedObservationId: string;
}) {
  const [reviewLabel, setReviewLabel] = useState<EventCandidateReviewLabel>(
    isCandidateReviewLabel(latestReview?.review_label) ? latestReview.review_label : "useful"
  );
  const [note, setNote] = useState(latestReview?.note ?? "");

  useEffect(() => {
    setReviewLabel(
      isCandidateReviewLabel(latestReview?.review_label) ? latestReview.review_label : "useful"
    );
    setNote(latestReview?.note ?? "");
  }, [latestReview, selectedObservationId]);

  const disabled = eventCandidateRunId === null || reviewSaving;

  return (
    <div className="marker-review-controls">
      <div className="marker-review-header">
        <strong>Operator review</strong>
        {latestReview !== null ? (
          <span className={`review-label-badge ${latestReview.review_label}`}>
            {formatReviewLabel(latestReview.review_label)}
          </span>
        ) : (
          <span className="mini-pill">no review</span>
        )}
      </div>
      <div className="marker-review-labels" role="group" aria-label="Candidate marker review">
        {markerReviewLabels.map((option) => (
          <button
            aria-pressed={reviewLabel === option.label}
            className={reviewLabel === option.label ? "selected" : ""}
            disabled={disabled}
            key={option.label}
            onClick={() => setReviewLabel(option.label)}
            type="button"
          >
            {option.text}
          </button>
        ))}
      </div>
      <label className="marker-review-note">
        <span>Review note</span>
        <textarea
          disabled={disabled}
          onChange={(event) => setNote(event.target.value)}
          placeholder="Optional operator note. Metadata only."
          value={note}
        />
      </label>
      {reviewError !== null ? <p className="marker-review-error">{reviewError}</p> : null}
      <div className="marker-review-actions">
        <button
          className="primary-button"
          disabled={disabled}
          onClick={() => onSaveReview(reviewLabel, note, latestReview?.id ?? null)}
          type="button"
        >
          {reviewSaving ? "Saving..." : "Save review"}
        </button>
        {latestReview !== null ? (
          <button
            className="quiet-button"
            disabled={reviewSaving}
            onClick={() => onDeleteReview(latestReview.id)}
            type="button"
          >
            Clear review
          </button>
        ) : null}
      </div>
      <p className="marker-review-warning">
        Review metadata only. Candidate evidence is preserved unchanged.
      </p>
    </div>
  );
}

function latestCandidateMarkerReview(
  reviews: EventCandidateReviewAnnotation[]
): EventCandidateReviewAnnotation | null {
  const markerReviews = reviews.filter(
    (review) => review.annotation_kind === "candidate_marker_review"
  );
  if (markerReviews.length === 0) {
    return null;
  }
  return [...markerReviews].sort((left, right) =>
    right.created_at.localeCompare(left.created_at)
  )[0];
}

function isCandidateReviewLabel(
  value: string | null | undefined
): value is EventCandidateReviewLabel {
  return markerReviewLabels.some((option) => option.label === value);
}

function formatReviewLabel(label: string): string {
  return label.replaceAll("_", " ").toUpperCase();
}
