# TOM v3 Blueprint 2 Completion Review

## Verdict

Blueprint 2 Status: COMPLETE.

Blueprint 2 proved that TOM v3 can compose persisted atomic detections into candidate temporal evidence, persist tracklet and track point observations with lineage to source detections, inspect that evidence across runs, review it with non-mutating annotations, query it through structured filters, and export it as a review dataset artifact without adjudicating correctness.

Blueprint 2 did not add pose, homography, bounce, hit, rally, point, scoring, identity proof, or truth promotion.

## What Blueprint 2 Proves

Blueprint 2 proves this TOM v3 temporal evidence flow:

```text
atomic detections
-> candidate tracklets
-> track point candidates
-> lineage
-> evidence bundle
-> query
-> review annotation
-> review dataset export
```

The flow remains observation-only:

- tracklet rows are candidate temporal groupings
- track point rows are candidate points in those groupings
- source detections remain immutable observations
- review annotations add human review evidence
- exports package evidence and provenance

## What Blueprint 2 Does Not Prove

Blueprint 2 does not prove:

- object identity
- trajectory correctness
- ball path correctness
- bounce occurrence
- hit occurrence
- rally state
- point state
- score
- model correctness

## Completion Review Questions

1. Is Blueprint 2 complete enough to close?
   Yes. The candidate temporal evidence layer can build, inspect, query, review, and export tracklet evidence.

2. What exactly does Blueprint 2 prove?
   It proves that persisted detections can become candidate temporal evidence with first-class observations, lineage, review annotations, structured query, viewer inspection, and export artifacts.

3. What does Blueprint 2 intentionally not prove?
   It does not prove detection correctness, identity, bounce, hit, rally, point, score, or any adjudicated result.

4. Are tracklets still represented as candidate evidence only?
   Yes. Tracklet rows and tracklet observation payloads use candidate/unverified status.

5. Do track points link back to source detections?
   Yes. Track point payloads include `source_detection_observation_id`, and lineage rows link source detections to track point candidate observations.

6. Does lineage preserve the chain `source detection -> track point -> tracklet`?
   Yes. `tracked_from` links source detection to track point, and `grouped_from` links track point to tracklet.

7. Can a user inspect a tracklet evidence bundle?
   Yes. `GET /tracklets/{tracklet_id}/evidence-bundle` and the viewer Tracklet Evidence panel expose the bundle.

8. Can a user query tracklet candidates?
   Yes. `POST /tracklets/query` supports structured filters for tracklet review.

9. Can a user annotate/review tracklets, track points, and source detections?
   Yes. Existing annotation APIs and viewer controls can target tracklet candidate, track point candidate, and source detection observation ids.

10. Can reviewed evidence be exported without converting reviews into truth?
    Yes. `export-tracklet-review-dataset` and `POST /tracklets/export-review-dataset` include annotations as review evidence and carry explicit candidate-only/no-adjudication warnings.

11. Does the viewer avoid truth/verified language?
    Yes. Tracklet viewer language uses candidate, source detection, evidence, review, and lineage terms.

12. Do docs avoid truth/verified/adjudication claims?
    Yes. Docs use those terms only to state non-goals and boundaries, not as implementation contracts.

13. Is pose still out of scope?
    Yes.

14. Is homography still out of scope?
    Yes, outside the synthetic placeholder work from earlier milestones.

15. Is bounce/hit/rally/point/scoring still out of scope?
    Yes.

16. Is real YOLO runtime still not integrated?
    Yes. Fixture detection is available, and YOLO runtime/assets remain documented as unavailable.

17. Is the next blueprint boundary clear?
    Yes. The recommended next blueprint is either real model runtime hardening or a pose/movement evidence layer, depending on user priority.

## Invariant Audit

| Invariant | Status | Coverage |
| --- | --- | --- |
| Tracklets are candidates. | Passed | `tests/test_tracklet_builder.py`, `tests/test_tracklet_evidence_bundle.py` |
| Track points are candidates. | Passed | `tests/test_tracklet_builder.py` |
| Tracklets have first-class observation rows. | Passed | `tests/test_tracklet_builder.py` |
| Track points have first-class observation rows. | Passed | `tests/test_tracklet_builder.py` |
| Source detections are not mutated by tracklet grouping. | Passed | `tests/test_blueprint_2_invariants.py` |
| Source detection to track point lineage exists. | Passed | `tests/test_tracklet_builder.py`, `tests/test_tracklet_evidence_bundle.py` |
| Track point to tracklet lineage exists. | Passed | `tests/test_tracklet_builder.py`, `tests/test_tracklet_evidence_bundle.py` |
| Track point frame/time values come from source detection frame/time values. | Passed | `tests/test_tracklet_builder.py` |
| Tracklet frame/time ranges derive from source detections. | Passed | `tests/test_tracklet_builder.py` |
| Evidence bundle reconstructs the multi-run chain. | Passed | `tests/test_tracklet_evidence_bundle.py` |
| Tracklet query does not create new facts. | Passed | Query is read-only; cross-flow immutability is covered by `tests/test_blueprint_2_invariants.py`. |
| Review annotations do not mutate observations. | Passed | `tests/test_tracklet_query_review.py`, `tests/test_blueprint_2_invariants.py` |
| Export artifacts preserve candidate/no-adjudication warning fields. | Passed | `tests/test_tracklet_review_export.py`, `tests/test_blueprint_2_invariants.py` |
| Export artifacts do not turn annotations into truth. | Passed | Export payload warnings and docs; `tests/test_tracklet_review_export.py` verifies warnings. |
| Viewer language remains candidate/evidence/review. | Passed | `docs/web/tracklet_evidence_viewer_v0.md`, `docs/web/tracklet_review_viewer_v0.md`, component text uses candidate/review terms. |
| Docs do not claim truth/adjudication. | Passed | Completion review and control-room docs preserve the boundary. |

## Naming Transition

The implementation branch and some historical files reference `1F` because tracklet grouping was originally planned as a Blueprint 1 extension. After Blueprint 1 was declared complete, the same work was reclassified as Blueprint 2A because temporal grouping begins a new conceptual layer.

The canonical interpretation is:

```text
Milestone 1F file/branch history
-> Milestone 2A Tracklet Candidate Foundation from Persisted Detections
```

Historical filenames are preserved to avoid churn. Current docs refer to this as Milestone 1F / 2A where needed.

## Known Limitations

- Tracklet grouping remains deterministic and simple.
- Viewer multi-run support is focused on evidence bundles, not a fused multi-run timeline.
- Exports reference frame artifact metadata and URIs; they do not copy frame image files.
- Real YOLO runtime/assets are still not available in this repo state.
- Review annotations use local/dev reviewer identity until auth exists.

## Recommended Next Blueprint

Recommended next blueprint: Blueprint 3 - Real Model Runtime / YOLO Observation Adapter.

Alternative next blueprint: Blueprint 3 - Pose Observation / Movement Evidence Layer.

Pose should remain outside Blueprint 2. If selected, it should begin as a new observation-only layer with the same provenance and non-adjudication rules.
