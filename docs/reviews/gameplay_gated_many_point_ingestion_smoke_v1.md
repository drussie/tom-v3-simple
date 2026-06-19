# Gameplay-Gated Many-Point Ingestion Smoke v1

Blueprint 42 creates a structural smoke/review surface for explicit many-point media entries.

The workflow reads a BP42 smoke manifest, validates local paths, runs the BP33 many-point
ingestion gate in dry-run mode, then builds BP38 gameplay segment candidates, BP39 routing plans,
BP40 perception execution plans, and BP41 replay timelines for each entry when requested.

The smoke report summarizes:

- validated entries
- entries with gameplay candidate windows
- blocked downstream windows
- review-required downstream windows
- perception execution/skipped windows
- replay timeline entry counts
- generated artifact paths
- fixture reuse warnings

The workflow is deliberately narrow. It does not auto-discover media, mutate model assets, mutate
regression baselines, run GPU/model inference by default, write observations, create labels, infer
tennis truth, or adjudicate evidence.

Generated `.data/exports/` files are local smoke outputs. The versioned contract under
`.data/contracts/gameplay_gated_many_point_smoke_contract_v1.json` is the durable artifact.
