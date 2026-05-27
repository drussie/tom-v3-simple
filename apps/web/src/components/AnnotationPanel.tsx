import type { HumanAnnotation, Observation } from "../lib/types";
import {
  annotationDisplayLabel,
  annotationNotes,
  booleanFlagText,
  keypointAnnotationText
} from "../lib/evidenceCopy";

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
        <p className="evidence-note">
          Annotations are review evidence. They do not mutate observations or change adapter/model
          output.
        </p>
        {annotations.length === 0 ? (
          <p className="empty-state">
            No review annotations yet. Review annotations can be added through the generic
            annotation API or seeded by `make demo`.
          </p>
        ) : null}
        {annotations.map((annotation) => (
          <div className="annotation-row" key={annotation.id}>
            <strong>{annotationDisplayLabel(annotation)}</strong>
            <span>{annotation.annotation_type}</span>
            <span className="mono">{annotation.created_by ?? "unknown"}</span>
            {annotation.frame_start !== null || annotation.frame_end !== null ? (
              <span>
                frame {annotation.frame_start ?? "n/a"}-{annotation.frame_end ?? "n/a"}
              </span>
            ) : null}
            {keypointAnnotationText(annotation) ? (
              <span>{keypointAnnotationText(annotation)}</span>
            ) : null}
            {annotationNotes(annotation) ? <p>{annotationNotes(annotation)}</p> : null}
            {booleanFlagText(annotation, "demo_seeded", "demo seeded") ? (
              <span>{booleanFlagText(annotation, "demo_seeded", "demo seeded")}</span>
            ) : null}
            {booleanFlagText(annotation, "review_only", "review only") ? (
              <span>{booleanFlagText(annotation, "review_only", "review only")}</span>
            ) : null}
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
