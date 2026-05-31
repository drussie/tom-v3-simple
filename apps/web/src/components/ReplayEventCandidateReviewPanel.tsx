"use client";

import type { ReplayMarkerSummary } from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayEventCandidateReviewPanelProps {
  markers: ReplayMarkerSummary[];
  selectedMarkerId: string | null;
  onSelectMarker: (marker: ReplayMarkerSummary) => void;
}

export function ReplayEventCandidateReviewPanel({
  markers,
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
  onSelectMarker
}: {
  isSelected: boolean;
  marker: ReplayMarkerSummary;
  onSelectMarker: (marker: ReplayMarkerSummary) => void;
}) {
  const isHit = marker.candidate_type === "hit_candidate";
  const markerLabel = isHit ? "HIT" : "BOUNCE";
  const fullMarkerLabel = isHit ? "HIT CANDIDATE" : "BOUNCE CANDIDATE";
  const sourceMethod =
    marker.source_method ?? marker.original_candidate_method ?? marker.candidate_method ?? "n/a";
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
    </button>
  );
}
