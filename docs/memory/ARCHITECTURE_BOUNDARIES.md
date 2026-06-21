# TOM v3 Architecture Boundaries

TOM v3 is an observation-first tennis evidence platform.

## Allowed

- Persist model, fixture, and runtime observations.
- Preserve provenance, confidence, source, frame/time, and lineage.
- Support visual replay.
- Support human review annotations.
- Export reviewed datasets.
- Run regression gates against frozen baselines.
- Add diagnostics and overlays.
- Add camera, court, and trajectory evidence.
- Add gameplay gating.
- Add review-guided calibration decision support.
- Add controlled runtime calibration governance artifacts.
- Add controlled runtime config changes only when explicitly authorized by a dedicated application
  execution blueprint.
- Add post-application verification and rollback controls after any controlled runtime config
  execution.

## Not Allowed Without Explicit Blueprint

- Declaring final tennis truth.
- Automatically adjudicating point outcome.
- Treating model output as ground truth.
- Overwriting evidence without lineage.
- Hiding uncertainty.
- Collapsing multiple candidates into one silent answer.
- Changing frozen baselines without explicit review.
- Modifying model weights.
- Creating production config.
- Applying runtime calibration without final gate, rollback package, and post-apply verification.
- Adding production claims without validation evidence.
- Claiming classifier accuracy, correctness, or generalization unless explicitly designed and
  validated.

## Controlled Calibration Boundary

Controlled runtime calibration may only proceed through explicit:

- change request
- dry run
- review packet
- human approval gate
- application plan
- staging
- final gate
- execution
- rollback
- post-application verification

## Design Principle

Evidence first.

Review second.

Regression third.

Controlled governance fourth.

Controlled execution only when explicitly gated.

Truth later, only if explicitly designed.
