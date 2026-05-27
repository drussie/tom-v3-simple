import type { Observation } from "../lib/types";
import { observationDisplayName } from "../lib/evidenceCopy";
import { formatConfidence, formatFrameRange } from "../lib/timeline";

interface ObservationListProps {
  observations: Observation[];
  selectedObservationId: string | null;
  onSelectObservation: (observationId: string) => void;
}

export function ObservationList({
  observations,
  selectedObservationId,
  onSelectObservation
}: ObservationListProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Observations</h2>
        <span className="mini-pill">{observations.length}</span>
      </div>
      <div className="panel-body observation-list">
        {observations.length === 0 ? (
          <p className="empty-state">
            No observations found for this run. Run `make demo` for the canonical fixture path, or
            run a detection/pose adapter for this media asset.
          </p>
        ) : null}
        {observations.map((observation) => (
          <button
            className={`observation-row${observation.id === selectedObservationId ? " selected" : ""}`}
            key={observation.id}
            onClick={() => onSelectObservation(observation.id)}
            type="button"
          >
            <span className="row-title">
              <strong>{observationDisplayName(observation)}</strong>
              <span className="mini-pill">{formatConfidence(observation.confidence)}</span>
            </span>
            <span className="row-meta">
              {observation.observation_family} /{" "}
              {formatFrameRange(observation.frame_start, observation.frame_end)}
            </span>
          </button>
        ))}
      </div>
    </section>
  );
}
