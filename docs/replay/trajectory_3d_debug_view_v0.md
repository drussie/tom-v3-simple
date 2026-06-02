# Trajectory 3D Debug View v0

The Replay Workstation 3D Debug View renders a compact top-down court-plane debug panel from
persisted `ball_trajectory_3d_candidate` rows.

The panel shows:

- declared court dimensions in meters
- candidate court-plane x/y samples
- an ordered candidate path through available samples
- height model and unknown-height counts
- selected marker diagnostic label and nearest 3D sample when available

It intentionally does not show:

- a true 3D ball arc
- synthetic height
- event truth
- in/out or score
- adjudication

Use a replay URL with `trajectory3dRunId=<trajectory_3d_run_id>` to load the panel data. When an
event candidate marker is selected, Blueprint 13 diagnostics can highlight the nearest 3D sample in
the panel.
