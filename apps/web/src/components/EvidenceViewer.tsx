"use client";

import { useEffect, useMemo, useState } from "react";

import { ArtifactPanel } from "./ArtifactPanel";
import { AnnotationPanel } from "./AnnotationPanel";
import { LineagePanel } from "./LineagePanel";
import { ObservationDetailPanel } from "./ObservationDetailPanel";
import { ObservationList } from "./ObservationList";
import { Timeline } from "./Timeline";
import { buildViewerModel } from "../lib/viewerData";
import type { ViewerRun } from "../lib/types";
import { formatFrameRange } from "../lib/timeline";

interface EvidenceViewerProps {
  viewerRun: ViewerRun;
}

export function EvidenceViewer({ viewerRun }: EvidenceViewerProps) {
  const model = useMemo(() => buildViewerModel(viewerRun), [viewerRun]);
  const [selectedObservationId, setSelectedObservationId] = useState<string | null>(
    model.defaultObservationId
  );

  useEffect(() => {
    setSelectedObservationId(model.defaultObservationId);
  }, [model.defaultObservationId]);

  const selectedObservation =
    selectedObservationId !== null ? model.observationsById.get(selectedObservationId) ?? null : null;
  const lineage =
    selectedObservationId !== null
      ? model.lineageByObservation.get(selectedObservationId) ?? { parents: [], children: [] }
      : { parents: [], children: [] };
  const artifacts =
    selectedObservationId !== null
      ? model.artifactsByObservation.get(selectedObservationId) ?? []
      : [];
  const annotations =
    selectedObservationId !== null
      ? model.annotationsByObservation.get(selectedObservationId) ?? []
      : [];
  const selectedFrame = selectedObservation?.frame_start ?? selectedObservation?.frame_end ?? null;

  return (
    <main className="viewer-shell">
      <header className="viewer-header">
        <div className="viewer-title">
          <p className="eyebrow">Visual Evidence Viewer</p>
          <h1>{viewerRun.run.run_name}</h1>
          <div className="meta-line">
            <span className="status-pill">{viewerRun.run.run_status}</span>
            <span className="mono">{viewerRun.run.id}</span>
            <span>{formatFrameRange(model.range.start, model.range.end)}</span>
          </div>
        </div>
        <div className="meta-line">
          <span className="mini-pill">{model.observations.length} observations</span>
          <span className="mini-pill">{viewerRun.tracklets.length} tracklets</span>
          <span className="mini-pill">{viewerRun.artifacts.length} artifacts</span>
        </div>
      </header>

      <div className="viewer-grid">
        <div className="main-column">
          <MediaPanel viewerRun={viewerRun} selectedFrame={selectedFrame} />
          <Timeline
            candidates={model.candidates}
            onSelectObservation={setSelectedObservationId}
            range={model.range}
            rows={model.rows}
            selectedObservationId={selectedObservationId}
          />
          <ObservationList
            observations={model.observations}
            onSelectObservation={setSelectedObservationId}
            selectedObservationId={selectedObservationId}
          />
        </div>
        <aside className="side-column">
          <ObservationDetailPanel observation={selectedObservation} />
          <LineagePanel lineage={lineage} />
          <ArtifactPanel artifacts={artifacts} />
          <AnnotationPanel annotations={annotations} selectedObservation={selectedObservation} />
        </aside>
      </div>
    </main>
  );
}

function MediaPanel({
  viewerRun,
  selectedFrame
}: {
  viewerRun: ViewerRun;
  selectedFrame: number | null;
}) {
  const media = viewerRun.media;
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Media</h2>
        <span className="mini-pill">selected frame {selectedFrame ?? "n/a"}</span>
      </div>
      <div className="panel-body media-grid">
        <div className="media-cell">
          <strong>Source</strong>
          <span>{media?.source_uri ?? "n/a"}</span>
        </div>
        <div className="media-cell">
          <strong>Dimensions</strong>
          <span>
            {media?.width ?? "n/a"} x {media?.height ?? "n/a"}
          </span>
        </div>
        <div className="media-cell">
          <strong>FPS</strong>
          <span>{media?.fps ?? "n/a"}</span>
        </div>
        <div className="media-cell">
          <strong>Duration</strong>
          <span>{media?.duration_ms ?? "n/a"} ms</span>
        </div>
        <div className="media-cell">
          <strong>Frames</strong>
          <span>{media?.frame_count ?? "n/a"}</span>
        </div>
      </div>
    </section>
  );
}
