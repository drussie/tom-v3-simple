import { EvidenceViewer } from "../../../components/EvidenceViewer";
import { fetchViewerRun } from "../../../lib/api";

interface RunPageProps {
  params: Promise<{
    runId: string;
  }>;
}

export default async function RunPage({ params }: RunPageProps) {
  const { runId } = await params;
  try {
    const viewerRun = await fetchViewerRun(runId);
    return <EvidenceViewer viewerRun={viewerRun} />;
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unable to load run";
    return (
      <main className="error-shell">
        <section className="error-panel">
          <p className="eyebrow">Run load failed</p>
          <h1>{runId}</h1>
          <p>{message}</p>
        </section>
      </main>
    );
  }
}
