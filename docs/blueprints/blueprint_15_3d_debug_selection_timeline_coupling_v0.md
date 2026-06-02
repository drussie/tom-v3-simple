# Blueprint 15 - 3D Debug Selection / Timeline Coupling v0

Status: complete

## Goal

Make the Replay Workstation 3D Debug View operationally useful as a display-only navigation and
inspection surface.

Blueprint 15 lets an operator:

- see the 3D candidate sample nearest to current replay time
- see local samples within the current time window
- click a 3D candidate sample to request replay seek
- inspect clicked 3D sample metadata
- highlight the nearest 3D sample linked to a selected hit/bounce marker diagnostic

## Scope

This milestone updates the existing Blueprint 14 panel. It does not add a new evidence layer,
backend mutation, CLI command, or persistence table.

## Boundaries

The 3D Debug View may request seek/select interactions through existing replay controls, but it
does not own playback time. It does not create true 3D reconstruction, verified height, hit truth,
bounce truth, in/out, score, accepted/rejected lifecycle, automatic correction, or adjudication.
