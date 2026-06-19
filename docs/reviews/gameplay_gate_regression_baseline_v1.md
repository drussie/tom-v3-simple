# Gameplay Gate Regression Baseline v1

Blueprint 43 creates a durable structural regression baseline for the gameplay gate path composed
from Blueprints 38-42.

The baseline freezes the expected local fixture-only summary for:

- TOM v1 gameplay classifier asset existence and fingerprint
- gameplay gate threshold, smoothing, and hysteresis settings
- BP42 smoke entry count and status distribution
- gameplay, non-gameplay, uncertain, downstream, perception, and replay timeline counts
- warning categories that keep fixture reuse and no-truth boundaries visible

The verifier compares the current fixture-safe gameplay gate summary with the frozen baseline and
reports drift separately from breaking drift. Model asset fingerprint or warning changes are
reported as drift; structural count/config/contract mismatches are breaking drift.

This is a regression/provenance gate only. It does not prove classifier accuracy, point detection,
line calling, score, player identity, production readiness, training truth, generalization, or
adjudication. Generated `.data/exports/` files remain local verification/report artifacts.
