# Blueprint 14 - 3D Trajectory Debug View v0

Status: complete

## Goal

Expose a display-only replay debug surface for existing `ball_trajectory_3d_candidate` evidence.
The view lets an operator inspect declared court-plane geometry, provisional metric x/y trajectory
samples, unknown height status, and the nearest 3D diagnostic sample for a selected hit/bounce
candidate marker.

## Scope

Blueprint 14 adds:

- replay `trajectory_3d_debug` read-model payload
- `trajectory3dRunId` replay URL/query support
- Replay Workstation 3D Debug View panel
- top-down SVG court-plane point/path display
- selected-marker nearest 3D sample highlight when Blueprint 13 diagnostics exist

## Boundaries

The debug view is display-only. It does not render a true 3D ball flight, fake height arcs, net
clearance, hit truth, bounce truth, in/out, score, accepted/rejected lifecycle, or adjudication.

Height remains explicitly unknown for the default `none_unknown` model. The view does not change
event candidate observations, marker arbitration, review annotations, point evidence snapshots, or
evaluation counts.
