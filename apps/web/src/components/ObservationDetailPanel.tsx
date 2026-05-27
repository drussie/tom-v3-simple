import type { Observation } from "../lib/types";
import {
  frameTimeOwner,
  observationDisplayName,
  observationEvidenceNote,
  sourceRuntime
} from "../lib/evidenceCopy";
import { formatConfidence, formatFrameRange } from "../lib/timeline";

interface ObservationDetailPanelProps {
  observation: Observation | null;
}

export function ObservationDetailPanel({ observation }: ObservationDetailPanelProps) {
  if (observation === null) {
    return (
      <section className="panel">
        <div className="panel-header">
          <h2>Observation Detail</h2>
        </div>
        <div className="panel-body">
          <p className="empty-state">
            No observation selected. Choose a detection observation, tracklet candidate, track point
            candidate, or pose observation to inspect payload, provenance, artifacts, and review
            context.
          </p>
        </div>
      </section>
    );
  }

  const typedDetail =
    observation.gameplay ?? observation.atomic ?? observation.derived ?? observation.pose;

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Observation Detail</h2>
        <span className="mini-pill">{observationDisplayName(observation)}</span>
      </div>
      <div className="panel-body detail-stack">
        <p className="evidence-note">{observationEvidenceNote(observation)}</p>
        <dl className="key-value">
          <dt>ID</dt>
          <dd className="mono">{observation.id}</dd>
          <dt>Type</dt>
          <dd>{observation.observation_type}</dd>
          <dt>Range</dt>
          <dd>{formatFrameRange(observation.frame_start, observation.frame_end)}</dd>
          <dt>Time</dt>
          <dd>
            {observation.timestamp_start_ms ?? "n/a"}-{observation.timestamp_end_ms ?? "n/a"} ms
          </dd>
          <dt>Confidence</dt>
          <dd>{formatConfidence(observation.confidence)}</dd>
          <dt>Space</dt>
          <dd>{observation.coordinate_space ?? "n/a"}</dd>
          <dt>Frame time owner</dt>
          <dd>{frameTimeOwner(observation) ?? "n/a"}</dd>
          <dt>Source runtime</dt>
          <dd>{sourceRuntime(observation) ?? "n/a"}</dd>
          <dt>Model</dt>
          <dd className="mono">{observation.model_id ?? "n/a"}</dd>
          <dt>Runtime config</dt>
          <dd className="mono">{observation.runtime_config_id ?? "n/a"}</dd>
          <dt>Run</dt>
          <dd className="mono">{observation.run_id}</dd>
        </dl>
        {typedDetail ? (
          <div>
            <h3 className="subhead">Typed Detail</h3>
            <pre className="json-box">{JSON.stringify(typedDetail, null, 2)}</pre>
          </div>
        ) : null}
        <div>
          <h3 className="subhead">Payload</h3>
          <pre className="json-box">{JSON.stringify(observation.payload_jsonb, null, 2)}</pre>
        </div>
      </div>
    </section>
  );
}
