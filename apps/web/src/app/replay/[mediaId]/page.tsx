import { ReplayWorkstation } from "../../../components/ReplayWorkstation";
import { fetchPointManifestIndex, fetchReplayInfo } from "../../../lib/api";
import type { ReplayMode } from "../../../lib/types";

interface ReplayPageProps {
  params: Promise<{
    mediaId: string;
  }>;
  searchParams: Promise<{
    detectionRunId?: string;
    mode?: string;
    trackletRunId?: string;
    poseRunId?: string;
    mainPlayerTrackRunId?: string;
    motionSmoothingRunId?: string;
    courtRunId?: string;
    courtTemporalPersistence?: string;
    courtPersistenceMaxGapMs?: string;
    homographyRunId?: string;
    projectionDiagnosticRunId?: string;
    courtProjectionRunId?: string;
    ballTrajectoryRunId?: string;
    eventCandidateRunId?: string;
    trajectory3dRunId?: string;
    cameraGeometryId?: string;
    viewPreset?: string;
  }>;
}

export default async function ReplayPage({ params, searchParams }: ReplayPageProps) {
  const { mediaId } = await params;
  const selectedRuns = await searchParams;
  const initialMode: ReplayMode = selectedRuns.mode === "stream_proxy" ? "stream_proxy" : "replay";
  try {
    const [replayInfo, pointManifestIndex] = await Promise.all([
      fetchReplayInfo(mediaId),
      fetchPointManifestIndex().catch(() => null)
    ]);
    return (
      <ReplayWorkstation
        initialMode={initialMode}
        pointManifestIndex={pointManifestIndex}
        replayInfo={replayInfo}
        selectedRuns={selectedRuns}
      />
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unable to load replay media";
    return (
      <main className="error-shell">
        <section className="error-panel">
          <p className="eyebrow">Replay media unavailable</p>
          <h1>{mediaId}</h1>
          <p>{message}</p>
          <p>
            Index media with <code>make demo</code> or <code>make index-media</code>, then open{" "}
            <code>/replay/&lt;media_id&gt;</code>.
          </p>
        </section>
      </main>
    );
  }
}
