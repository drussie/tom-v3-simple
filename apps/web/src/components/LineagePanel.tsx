import type { LineageRow } from "../lib/types";
import { relationshipDescription } from "../lib/evidenceCopy";

interface LineagePanelProps {
  lineage: {
    parents: LineageRow[];
    children: LineageRow[];
  };
}

export function LineagePanel({ lineage }: LineagePanelProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Lineage</h2>
        <span className="mini-pill">{lineage.parents.length + lineage.children.length}</span>
      </div>
      <div className="panel-body lineage-list">
        {lineage.parents.length === 0 && lineage.children.length === 0 ? (
          <p className="empty-state">
            No lineage rows for this observation. Some root observations, such as unassociated
            full-frame pose observations or fixture source outputs, may have no parent lineage.
          </p>
        ) : null}
        {lineage.parents.map((row) => (
          <LineageItem key={row.id} label="Parent" row={row} relatedId={row.parent_observation_id} />
        ))}
        {lineage.children.map((row) => (
          <LineageItem key={row.id} label="Child" row={row} relatedId={row.child_observation_id} />
        ))}
      </div>
    </section>
  );
}

function LineageItem({
  row,
  label,
  relatedId
}: {
  row: LineageRow;
  label: string;
  relatedId: string;
}) {
  return (
    <div className="lineage-row">
      <strong>
        {label} / {row.relationship_type}
      </strong>
      <span>{relationshipDescription(row.relationship_type)}</span>
      <span className="mono">{relatedId}</span>
    </div>
  );
}
