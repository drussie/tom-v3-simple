import { ReplayVideoPlayer } from "../../../components/ReplayVideoPlayer";
import { fetchReplayInfo } from "../../../lib/api";
import type { ReplayInfo, ReplayRunSummary } from "../../../lib/types";

interface ReplayPageProps {
  params: Promise<{
    mediaId: string;
  }>;
  searchParams: Promise<{
    detectionRunId?: string;
    trackletRunId?: string;
    poseRunId?: string;
  }>;
}

export default async function ReplayPage({ params, searchParams }: ReplayPageProps) {
  const { mediaId } = await params;
  const selectedRuns = await searchParams;
  try {
    const replayInfo = await fetchReplayInfo(mediaId);
    return <ReplayWorkstation replayInfo={replayInfo} selectedRuns={selectedRuns} />;
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

function ReplayWorkstation({
  replayInfo,
  selectedRuns
}: {
  replayInfo: ReplayInfo;
  selectedRuns: {
    detectionRunId?: string;
    trackletRunId?: string;
    poseRunId?: string;
  };
}) {
  return (
    <main className="viewer-shell replay-shell">
      <header className="viewer-header">
        <div className="viewer-title">
          <p className="eyebrow">TOM v3 Replay Workstation</p>
          <h1>Video replay timeline foundation</h1>
          <div className="meta-line">
            <span className="status-pill">observation-only</span>
            <span className="mini-pill">no adjudication</span>
            <span className="mono">{replayInfo.media_id}</span>
          </div>
        </div>
        <div className="meta-line">
          <span className="mini-pill">{replayInfo.frame_time_mode} frame/time</span>
          <span className="mini-pill">{replayInfo.available_runs.detection.length} detection runs</span>
          <span className="mini-pill">{replayInfo.available_runs.pose.length} pose runs</span>
        </div>
      </header>

      <div className="replay-grid">
        <div className="main-column">
          <ReplayVideoPlayer replayInfo={replayInfo} />
          <SelectedRunContext replayInfo={replayInfo} selectedRuns={selectedRuns} />
        </div>
        <aside className="side-column">
          <ReplayMediaPanel replayInfo={replayInfo} />
          <AvailableRunsPanel replayInfo={replayInfo} />
          <section className="panel">
            <div className="panel-header">
              <h2>Overlay Layers</h2>
              <span className="mini-pill">future milestones</span>
            </div>
            <div className="panel-body">
              <p className="empty-state">
                Detection, tracklet candidate, and pose observation playback overlays arrive in
                6B/6C. This page only synchronizes indexed video playback to TOM media-owned
                frame/time.
              </p>
            </div>
          </section>
        </aside>
      </div>
    </main>
  );
}

function ReplayMediaPanel({ replayInfo }: { replayInfo: ReplayInfo }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Media</h2>
        <span className="mini-pill">indexed video</span>
      </div>
      <div className="panel-body replay-media-detail">
        <DetailRow label="media id" value={replayInfo.media_id} />
        <DetailRow label="source" value={replayInfo.source_uri} />
        <DetailRow label="dimensions" value={`${replayInfo.width ?? "n/a"} x ${replayInfo.height ?? "n/a"}`} />
        <DetailRow label="duration_ms" value={replayInfo.duration_ms?.toString() ?? "n/a"} />
        <DetailRow label="fps" value={replayInfo.fps?.toString() ?? "n/a"} />
        <DetailRow label="frame_count" value={replayInfo.frame_count?.toString() ?? "n/a"} />
        <DetailRow label="video endpoint" value={replayInfo.video_url} />
      </div>
    </section>
  );
}

function AvailableRunsPanel({ replayInfo }: { replayInfo: ReplayInfo }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Available Run Context</h2>
        <span className="mini-pill">persisted evidence</span>
      </div>
      <div className="panel-body run-group-list">
        <RunGroup title="Detection observations" runs={replayInfo.available_runs.detection} />
        <RunGroup title="Tracklet candidates" runs={replayInfo.available_runs.tracklet} />
        <RunGroup title="Pose observations" runs={replayInfo.available_runs.pose} />
        <RunGroup title="Gameplay/view-state observations" runs={replayInfo.available_runs.gameplay} />
      </div>
    </section>
  );
}

function SelectedRunContext({
  replayInfo,
  selectedRuns
}: {
  replayInfo: ReplayInfo;
  selectedRuns: {
    detectionRunId?: string;
    trackletRunId?: string;
    poseRunId?: string;
  };
}) {
  const selected = [
    ["detection", selectedRuns.detectionRunId, replayInfo.available_runs.detection],
    ["tracklet candidate", selectedRuns.trackletRunId, replayInfo.available_runs.tracklet],
    ["pose observation", selectedRuns.poseRunId, replayInfo.available_runs.pose]
  ] as const;

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Selected Run Context</h2>
        <span className="mini-pill">optional</span>
      </div>
      <div className="panel-body run-group-list">
        {selected.map(([label, runId, runs]) => (
          <SelectedRunRow key={label} label={label} runId={runId} runs={runs} />
        ))}
        <p className="empty-state">
          Run query parameters only select replay context in 6A. Overlay playback comes later.
        </p>
      </div>
    </section>
  );
}

function RunGroup({ title, runs }: { title: string; runs: ReplayRunSummary[] }) {
  return (
    <div className="run-group">
      <h3>{title}</h3>
      {runs.length === 0 ? (
        <p className="empty-state compact">
          No {title.toLowerCase()} are attached to this media yet.
        </p>
      ) : (
        <ul>
          {runs.map((run) => (
            <li key={run.run_id}>
              <strong>{run.run_name}</strong>
              <span className="mono">{run.run_id}</span>
              <span>
                {run.run_status} · {run.observation_count} observations
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function SelectedRunRow({
  label,
  runId,
  runs
}: {
  label: string;
  runId?: string;
  runs: ReplayRunSummary[];
}) {
  const run = runs.find((candidate) => candidate.run_id === runId);
  return (
    <div className="selected-run-row">
      <strong>{label}</strong>
      {runId === undefined ? (
        <span className="empty-state compact">No run selected.</span>
      ) : run === undefined ? (
        <span className="empty-state compact">Selected run is not available for this media.</span>
      ) : (
        <span>
          {run.run_name} · {run.observation_count} observations
        </span>
      )}
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="detail-row">
      <strong>{label}</strong>
      <span className="mono">{value}</span>
    </div>
  );
}
