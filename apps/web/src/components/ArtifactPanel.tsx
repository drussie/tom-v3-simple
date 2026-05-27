import type { EvidenceArtifact } from "../lib/types";
import { exportRecordCount, isReviewExportArtifact } from "../lib/evidenceCopy";
import { formatFrameRange } from "../lib/timeline";

interface ArtifactPanelProps {
  artifacts: EvidenceArtifact[];
}

export function ArtifactPanel({ artifacts }: ArtifactPanelProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Artifacts</h2>
        <span className="mini-pill">{artifacts.length}</span>
      </div>
      <div className="panel-body artifact-list">
        {artifacts.length === 0 ? (
          <p className="empty-state">
            No evidence artifacts found for this observation. Artifacts may need to be generated
            separately, for example with `extract-frame-artifacts`.
          </p>
        ) : null}
        {artifacts.map((artifact) => (
          <div className="artifact-row" key={artifact.id}>
            <strong>{artifact.artifact_type}</strong>
            <span>{formatFrameRange(artifact.frame_start, artifact.frame_end)}</span>
            <span>target observation: {artifact.target_observation_id ?? "run/media artifact"}</span>
            {isReviewExportArtifact(artifact) ? <span>{exportRecordCount(artifact)}</span> : null}
            <span className="mono">{artifact.uri}</span>
            {artifact.checksum !== null ? (
              <span className="mono">sha256 {artifact.checksum}</span>
            ) : null}
            {artifact.created_at !== null ? <span>created {artifact.created_at}</span> : null}
          </div>
        ))}
      </div>
    </section>
  );
}
