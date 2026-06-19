# Gameplay Gate Review Dataset Export v1

Blueprint 44 creates a structural review dataset export for the gameplay gate path composed from
Blueprints 38-43.

The dataset bundles review entries for gameplay, non-gameplay, uncertain, and filtered segment
candidates with:

- replay links and segment time windows
- source media path, source artifact paths, and source contract refs
- TOM v1 gameplay classifier asset provenance
- threshold, smoothing, and hysteresis settings
- routing, execution, replay timeline, and regression context where available
- blank human review metadata fields for future review workflows
- warning and non-claim fields that keep the export outside truth/adjudication semantics

The validator checks structure, allowed review metadata values, source contract refs, and exact
forbidden fields/values. The report summarizes entry counts, pending human review, status
distributions, ambiguity fields, missing source context, model asset provenance, and warnings.

This is a human review dataset export only. It does not prove classifier correctness, create
review labels, detect points, call lines, score, identify players, relabel automatically, create
training truth, claim production readiness or generalization, or adjudicate evidence. Generated
`.data/exports/` files remain local artifacts.
