import type { CandidateMarker, TimelineRange } from "../lib/types";
import { formatConfidence, frameToPercent } from "../lib/timeline";

interface CandidateMarkersProps {
  candidates: CandidateMarker[];
  range: TimelineRange;
  selectedObservationId: string | null;
  onSelectObservation: (observationId: string) => void;
}

export function CandidateMarkers({
  candidates,
  range,
  selectedObservationId,
  onSelectObservation
}: CandidateMarkersProps) {
  return (
    <div className="timeline-row">
      <div className="timeline-label">Candidates</div>
      <div className="timeline-track candidate-track">
        {candidates.map((candidate) => (
          <button
            aria-label={`${candidate.label} at frame ${candidate.frame}`}
            className={`candidate-marker${
              candidate.observationId === selectedObservationId ? " selected" : ""
            }`}
            key={candidate.id}
            onClick={() => onSelectObservation(candidate.observationId)}
            style={{ left: `${frameToPercent(candidate.frame, range)}%` }}
            title={`${candidate.label} ${formatConfidence(candidate.confidence)}`}
            type="button"
          >
            <span>{candidate.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
