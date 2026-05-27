import {
  exportRecordCount,
  isReviewExportArtifact,
  observationDisplayName
} from "../lib/evidenceCopy";
import type { Observation, ViewerRun } from "../lib/types";

interface RunEvidenceSummaryProps {
  viewerRun: ViewerRun;
}

export function RunEvidenceSummary({ viewerRun }: RunEvidenceSummaryProps) {
  const observationCounts = countObservations(viewerRun.observations);
  const exportArtifacts = viewerRun.artifacts.filter(isReviewExportArtifact);

  return (
    <section className="panel run-summary-panel">
      <div className="panel-header">
        <h2>Run Evidence Summary</h2>
        <span className="mini-pill">{viewerRun.steps.length} processing steps</span>
      </div>
      <div className="panel-body run-summary-body">
        <p className="evidence-note">
          This viewer shows persisted observation evidence, lineage, artifacts, and review context.
          It does not decide tennis events, scores, identity, or movement meaning.
        </p>
        <div className="run-summary-grid">
          <SummaryCell label="Processing run" value={viewerRun.run.id} mono />
          <SummaryCell label="Run status" value={viewerRun.run.run_status} />
          <SummaryCell
            label="Runtime config"
            value={viewerRun.run.runtime_config_id ?? "n/a"}
            mono
          />
          <SummaryCell label="Observation rows" value={String(viewerRun.observations.length)} />
          <SummaryCell label="Lineage rows" value={String(viewerRun.lineage.length)} />
          <SummaryCell label="Review annotations" value={String(viewerRun.annotations.length)} />
        </div>
        <div className="summary-section">
          <h3>Observation Types</h3>
          {observationCounts.length === 0 ? (
            <p className="empty-state">
              No observations found for this run. Run `make demo`, `run-detection-adapter`, or
              `run-pose-adapter` to create local evidence.
            </p>
          ) : (
            <div className="summary-pill-row">
              {observationCounts.map((row) => (
                <span className="summary-pill" key={row.label}>
                  {row.label}: {row.count}
                </span>
              ))}
            </div>
          )}
        </div>
        <div className="summary-section">
          <h3>Review Dataset Exports</h3>
          {exportArtifacts.length === 0 ? (
            <p className="empty-state">
              No review dataset export artifact is visible for this run. Run
              `export-pose-review-dataset`, `export-tracklet-review-dataset`, or `make demo`; demo
              output prints export paths.
            </p>
          ) : (
            <div className="export-summary-list">
              {exportArtifacts.map((artifact) => (
                <div className="export-summary-row" key={artifact.id}>
                  <strong>{artifact.artifact_type.replaceAll("_", " ")}</strong>
                  <span>{exportRecordCount(artifact)}</span>
                  <span className="mono">{artifact.id}</span>
                  <span className="mono">{artifact.uri}</span>
                  {artifact.checksum !== null ? (
                    <span className="mono">sha256 {artifact.checksum}</span>
                  ) : null}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

function countObservations(observations: Observation[]): Array<{ label: string; count: number }> {
  const counts = new Map<string, { label: string; count: number }>();
  for (const observation of observations) {
    const label = observationDisplayName(observation);
    const current = counts.get(label) ?? { label, count: 0 };
    current.count += 1;
    counts.set(label, current);
  }
  return [...counts.values()].sort((left, right) => left.label.localeCompare(right.label));
}

function SummaryCell({
  label,
  mono = false,
  value
}: {
  label: string;
  mono?: boolean;
  value: string;
}) {
  return (
    <div className="media-cell">
      <strong>{label}</strong>
      <span className={mono ? "mono" : undefined}>{value}</span>
    </div>
  );
}
