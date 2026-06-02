# Trajectory 3D Debug Selection / Timeline Coupling v0

The 3D Debug View now couples existing 3D candidate samples to replay time and selected markers.

The panel highlights:

- all candidate samples
- samples in the local current-time window
- the current-time nearest sample
- the selected-marker nearest diagnostic sample
- a clicked selected sample

Clicking a sample requests a replay seek to that sample timestamp and displays sample metadata.
This is a UI request through existing replay controls; the debug panel does not own time.

The panel continues to show `height_model=none_unknown`, `Height: unknown`, and true 3D
reconstruction as unavailable in v0. It does not render true 3D ball flight, change hit/bounce
candidates, decide in/out, score, or adjudicate.
