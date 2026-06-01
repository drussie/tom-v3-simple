# Blueprint 13 3D-Assisted Event Candidate Diagnostics v0 Report

## Summary

Implemented a diagnostic-only bridge from final visible hit/bounce event markers to nearby
Blueprint 12 3D ball trajectory candidate samples.

## Added

- `event_candidate_3d_diagnostic` persistence table
- schema contract and conservative status/label validation
- `build-event-candidate-3d-diagnostics` worker CLI
- `tom-v1-build-event-candidate-3d-diagnostics` Make helper
- replay compact diagnostics and marker-summary attachment
- point evidence snapshot diagnostic summary
- point candidate evaluation diagnostic summary
- Marker Inspector 3D Diagnostic block

## Boundary

The diagnostics do not change hit/bounce generation, marker arbitration, candidate counts, review
annotations, source evidence, 3D trajectory candidates, in/out, score, or adjudication.

## Remaining Limitations

- Blueprint 12 default height model keeps ball height unknown.
- v0 uses conservative neutral labels unless future bounded 3D evidence supports a stronger
  diagnostic.
- No 3D visualization is added.
