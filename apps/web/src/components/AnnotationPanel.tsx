import type { HumanAnnotation, Observation } from "../lib/types";

interface AnnotationPanelProps {
  annotations: HumanAnnotation[];
  selectedObservation: Observation | null;
}

export function AnnotationPanel({ annotations, selectedObservation }: AnnotationPanelProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Annotations</h2>
        <span className="mini-pill">{annotations.length}</span>
      </div>
      <div className="panel-body annotation-list">
        {annotations.length === 0 ? <p className="empty-state">No annotations linked.</p> : null}
        {annotations.map((annotation) => (
          <div className="annotation-row" key={annotation.id}>
            <strong>{annotation.annotation_type}</strong>
            <span className="mono">{annotation.created_by ?? "unknown"}</span>
          </div>
        ))}
        <textarea
          aria-label="Annotation payload"
          disabled
          placeholder={selectedObservation ? "Annotation payload" : "Select an observation"}
          rows={3}
        />
        <button className="quiet-button" disabled type="button">
          Add annotation
        </button>
      </div>
    </section>
  );
}
