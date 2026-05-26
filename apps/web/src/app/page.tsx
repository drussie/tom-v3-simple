import { RunLauncher } from "../components/RunLauncher";

export default function HomePage() {
  return (
    <main className="home-shell">
      <section className="home-panel">
        <div>
          <p className="eyebrow">TOM v3 Simple</p>
          <h1>Visual Evidence Viewer</h1>
        </div>
        <RunLauncher />
      </section>
    </main>
  );
}
