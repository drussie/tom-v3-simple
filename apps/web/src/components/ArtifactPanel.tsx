import type { EvidenceArtifact } from "../lib/types";
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
        {artifacts.length === 0 ? <p className="empty-state">No artifacts linked.</p> : null}
        {artifacts.map((artifact) => (
          <div className="artifact-row" key={artifact.id}>
            <strong>{artifact.artifact_type}</strong>
            <div className="row-meta">{formatFrameRange(artifact.frame_start, artifact.frame_end)}</div>
            <div className="mono">{artifact.uri}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
