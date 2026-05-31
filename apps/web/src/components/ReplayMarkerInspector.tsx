"use client";

import type { ReplayMarkerSummary } from "../lib/types";
import { formatConfidence } from "../lib/timeline";

interface ReplayMarkerInspectorProps {
  selectedMarker: ReplayMarkerSummary | null;
  markerCount: number;
}

export function ReplayMarkerInspector({
  selectedMarker,
  markerCount
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
