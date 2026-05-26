import type { TimelineRange, TimelineRow, TimelineSegment } from "../lib/types";
import { formatConfidence, segmentStyle } from "../lib/timeline";

interface TimelineBandProps {
  row: TimelineRow;
  range: TimelineRange;
  selectedObservationId: string | null;
  onSelectObservation: (observationId: string) => void;
}

export function TimelineBand({
  row,
  range,
  selectedObservationId,
  onSelectObservation
}: TimelineBandProps) {
  return (
    <div className="timeline-row">
      <div className="timeline-label">{row.label}</div>
      <div className="timeline-track">
        {row.segments.map((segment) => (
          <SegmentButton
            key={segment.id}
            onSelectObservation={onSelectObservation}
            range={range}
            segment={segment}
            selectedObservationId={selectedObservationId}
          />
        ))}
      </div>
    </div>
  );
}

function SegmentButton({
  segment,
  range,
  selectedObservationId,
  onSelectObservation
}: {
  segment: TimelineSegment;
  range: TimelineRange;
  selectedObservationId: string | null;
  onSelectObservation: (observationId: string) => void;
}) {
  const canSelect = segment.observationId !== undefined;
  const selected = segment.observationId === selectedObservationId;
  return (
    <button
      aria-label={`${segment.label} ${formatConfidence(segment.confidence)}`}
      className={`timeline-segment state-${stateClass(segment.state)}${selected ? " selected" : ""}`}
      disabled={!canSelect}
      onClick={() => {
        if (segment.observationId) {
          onSelectObservation(segment.observationId);
        }
      }}
      style={segmentStyle(segment.frameStart, segment.frameEnd, range)}
      type="button"
    >
      <span>{segment.label}</span>
    </button>
  );
}

function stateClass(state: string): string {
  return state.replaceAll(" ", "_").replaceAll("-", "_");
}
