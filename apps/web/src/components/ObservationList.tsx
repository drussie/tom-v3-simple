import type { Observation } from "../lib/types";
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
        {observations.map((observation) => (
          <button
            className={`observation-row${observation.id === selectedObservationId ? " selected" : ""}`}
            key={observation.id}
            onClick={() => onSelectObservation(observation.id)}
            type="button"
          >
            <span className="row-title">
              <strong>{observation.observation_type}</strong>
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
