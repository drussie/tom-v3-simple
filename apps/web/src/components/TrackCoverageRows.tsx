import { TimelineBand } from "./TimelineBand";
import type { TimelineRange, TimelineRow } from "../lib/types";

interface TrackCoverageRowsProps {
  rows: TimelineRow[];
  range: TimelineRange;
  selectedObservationId: string | null;
  onSelectObservation: (observationId: string) => void;
}

export function TrackCoverageRows({
  rows,
  range,
  selectedObservationId,
  onSelectObservation
}: TrackCoverageRowsProps) {
  return (
    <>
      {rows.map((row) => (
        <TimelineBand
          key={row.id}
          onSelectObservation={onSelectObservation}
          range={range}
          row={row}
          selectedObservationId={selectedObservationId}
        />
      ))}
    </>
  );
}
