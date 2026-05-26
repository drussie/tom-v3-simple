"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export function RunLauncher() {
  const [runId, setRunId] = useState("");
  const router = useRouter();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextRunId = runId.trim();
    if (nextRunId.length > 0) {
      router.push(`/runs/${nextRunId}`);
    }
  }

  return (
    <form className="run-launcher" onSubmit={handleSubmit}>
      <input
        aria-label="Run ID"
        onChange={(event) => setRunId(event.target.value)}
        placeholder="Run ID"
        value={runId}
      />
      <button className="primary-button" type="submit">
        Open run
      </button>
    </form>
  );
}
