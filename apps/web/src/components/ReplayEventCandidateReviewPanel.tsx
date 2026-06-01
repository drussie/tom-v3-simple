"use client";

import type { EventCandidateReviewAnnotation, ReplayMarkerSummary } from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayEventCandidateReviewPanelProps {
  markers: ReplayMarkerSummary[];
  reviewsByObservationId: Record<string, EventCandidateReviewAnnotation[]>;
  reviewSummary: Record<string, number>;
  reviewError: string | null;
  reviewLoading: boolean;
  selectedMarkerId: string | null;
  onSelectMarker: (marker: ReplayMarkerSummary) => void;
}

export function ReplayEventCandidateReviewPanel({
  markers,
  reviewsByObservationId,
  reviewSummary,
  reviewError,
  reviewLoading,
  selectedMarkerId,
  onSelectMarker
}: ReplayEventCandidateReviewPanelProps) {
  return (
    <section className="panel event-candidate-review-panel">
      <div className="panel-header">
        <h2>Event Candidate Review</h2>
        <span className="mini-pill">{markers.length} final markers</span>
      </div>
      <div className="panel-body event-candidate-review-body">
        <ReviewSummaryStrip
          reviewError={reviewError}
          reviewLoading={reviewLoading}
          reviewSummary={reviewSummary}
        />
        {markers.length === 0 ? (
          <>
            <p className="empty-state compact">
              No final event candidates available. Run hit/bounce candidate generation and open
              replay with eventCandidateRunId.
            </p>
            <p className="event-candidate-review-warning">
              Candidate evidence only - not truth, not score, not in/out.
            </p>
          </>
        ) : (
          <>
            <div className="event-candidate-review-list" role="list">
              {markers.map((marker) => (
                <EventCandidateReviewRow
                  isSelected={marker.observation_id === selectedMarkerId}
                  key={marker.observation_id}
                  marker={marker}
                  onSelectMarker={onSelectMarker}
                  reviews={reviewsByObservationId[marker.observation_id] ?? []}
                />
              ))}
            </div>
            <p className="event-candidate-review-warning">
              Candidate evidence only - not truth, not score, not in/out.
            </p>
          </>
        )}
      </div>
    </section>
  );
}

function EventCandidateReviewRow({
  isSelected,
  marker,
  onSelectMarker,
  reviews
}: {
  isSelected: boolean;
  marker: ReplayMarkerSummary;
  onSelectMarker: (marker: ReplayMarkerSummary) => void;
  reviews: EventCandidateReviewAnnotation[];
}) {
  const isHit = marker.candidate_type === "hit_candidate";
  const markerLabel = isHit ? "HIT" : "BOUNCE";
  const fullMarkerLabel = isHit ? "HIT CANDIDATE" : "BOUNCE CANDIDATE";
  const sourceMethod =
    marker.source_method ?? marker.original_candidate_method ?? marker.candidate_method ?? "n/a";
  const latestReview = latestCandidateMarkerReview(reviews);
  return (
    <button
      aria-label={`${fullMarkerLabel} marker ${marker.index} frame ${marker.frame}`}
      className={`event-candidate-review-row ${isSelected ? "selected" : ""} ${
        isHit ? "hit" : "bounce"
      }`}
      onClick={() => onSelectMarker(marker)}
      type="button"
    >
      <span className="event-candidate-review-index">#{marker.index}</span>
      <span className={`marker-type-pill review-type ${isHit ? "hit" : "bounce"}`}>
        {markerLabel}
      </span>
      <span className="event-candidate-review-time">
        frame {marker.frame} / {marker.timestamp_ms} ms
      </span>
      <span className="event-candidate-review-meta">
        <strong>source</strong>
        <span>{sourceMethod}</span>
      </span>
      <span className="event-candidate-review-meta compact">
        <strong>decision</strong>
        <span>{marker.arbitration_decision ?? "n/a"}</span>
      </span>
      <span className="event-candidate-review-confidence">
        {formatConfidence(marker.confidence ?? null)}
      </span>
      {latestReview !== null ? (
        <span className={`review-label-badge row-badge ${latestReview.review_label}`}>
          {formatReviewLabel(latestReview.review_label)}
        </span>
      ) : null}
    </button>
  );
}

function ReviewSummaryStrip({
  reviewError,
  reviewLoading,
  reviewSummary
}: {
  reviewError: string | null;
  reviewLoading: boolean;
  reviewSummary: Record<string, number>;
}) {
  return (
    <div className="event-review-summary-strip">
      <span className="mini-pill">
        {reviewLoading ? "loading reviews" : `${reviewSummary.total_reviews ?? 0} reviews`}
      </span>
      <span className="mini-pill">{reviewSummary.useful ?? 0} useful</span>
      <span className="mini-pill">{reviewSummary.wrong ?? 0} wrong</span>
      <span className="mini-pill">{reviewSummary.unclear ?? 0} unclear</span>
      <span className="mini-pill">{reviewSummary.needs_review ?? 0} needs review</span>
      <span className="mini-pill">
        {reviewSummary.missing_candidate_note ?? 0} missing notes
      </span>
      {reviewError !== null ? <span className="review-error-pill">{reviewError}</span> : null}
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

function formatReviewLabel(label: string): string {
  return label.replaceAll("_", " ").toUpperCase();
}
