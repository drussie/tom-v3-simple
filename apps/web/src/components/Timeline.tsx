import { CandidateMarkers } from "./CandidateMarkers";
import { TimelineBand } from "./TimelineBand";
import { TrackCoverageRows } from "./TrackCoverageRows";
import type { CandidateMarker, TimelineRange, TimelineRow } from "../lib/types";

interface TimelineProps {
  rows: TimelineRow[];
  candidates: CandidateMarker[];
  range: TimelineRange;
  selectedObservationId: string | null;
  onSelectObservation: (observationId: string) => void;
}

export function Timeline({
  rows,
  candidates,
  range,
  selectedObservationId,
  onSelectObservation
}: TimelineProps) {
  const gameplayRow = rows.find((row) => row.id === "gameplay");
  const homographyRow = rows.find((row) => row.id === "homography");
  const trackRows = rows.filter((row) => row.id !== "gameplay" && row.id !== "homography");

  return (
    <section className="panel timeline-panel">
      <div className="panel-header">
        <h2>Timeline</h2>
        <span className="mini-pill">
          {range.start}-{range.end}
        </span>
      </div>
      <div className="timeline-axis">
        <span />
        <div className="axis-track">
          <span>{range.start}</span>
          <span>{Math.round((range.start + range.end) / 2)}</span>
          <span>{range.end}</span>
        </div>
      </div>
      <div className="timeline-body">
        {gameplayRow ? (
          <TimelineBand
            onSelectObservation={onSelectObservation}
            range={range}
            row={gameplayRow}
            selectedObservationId={selectedObservationId}
          />
        ) : null}
        <TrackCoverageRows
          onSelectObservation={onSelectObservation}
          range={range}
          rows={trackRows}
          selectedObservationId={selectedObservationId}
        />
        {homographyRow ? (
          <TimelineBand
            onSelectObservation={onSelectObservation}
            range={range}
            row={homographyRow}
            selectedObservationId={selectedObservationId}
          />
        ) : null}
        <CandidateMarkers
          candidates={candidates}
          onSelectObservation={onSelectObservation}
          range={range}
          selectedObservationId={selectedObservationId}
        />
      </div>
    </section>
  );
}
