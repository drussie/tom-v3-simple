from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any, Literal

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.court import COURT_TEMPLATE_NAME, COURT_TEMPLATE_VERSION
from tom_v3_schema.enums import (
    CoordinateSpace,
    ObservationFamily,
    ObservationGranularity,
    RelationshipType,
)
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

BALL_TRAJECTORY_OBSERVATION_TYPE = "ball_trajectory_court_candidate"
BALL_COURT_PROJECTION_OBSERVATION_TYPE = "ball_court_projection_candidate"
MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE = "main_player_court_projection_candidate"
HIT_CANDIDATE_OBSERVATION_TYPE = "hit_candidate"
BOUNCE_CANDIDATE_OBSERVATION_TYPE = "bounce_candidate"
EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE = (
    "event_candidate_rejection_diagnostic"
)
EVENT_CANDIDATE_OBSERVATION_TYPES = {
    HIT_CANDIDATE_OBSERVATION_TYPE,
    BOUNCE_CANDIDATE_OBSERVATION_TYPE,
    EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE,
}
HIT_CANDIDATE_METHOD = "net_axis_reversal_player_proximity_hit_candidate_v024"
HIT_FALLBACK_CANDIDATE_METHOD = (
    "player_proximate_speed_reduction_hit_candidate_fallback_v024"
)
NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD = "net_axis_reversal_hit_candidate_v025"
BOUNCE_CANDIDATE_METHOD = "image_vertical_proxy_speed_reduction_bounce_candidate_v024"
BOUNCE_FALLBACK_CANDIDATE_METHOD = (
    "image_vertical_proxy_speed_reduction_bounce_candidate_v024_fallback"
)
PLAYER_ANCHORED_HIT_CANDIDATE_METHOD = (
    "player_anchored_contact_zone_net_axis_reversal_hit_candidate_v024"
)
SIDE_ZONE_SEQUENCE_HIT_METHOD = "side_zone_sequence_hit_candidate_v024"
SIDE_ZONE_SEQUENCE_BOUNCE_METHOD = "side_zone_sequence_bounce_candidate_v024"
EVENT_CANDIDATE_METHOD = (
    "net_axis_reversal_hit_recall_candidate_evidence_v025"
)
COURT_SIDE_SPLIT_Y = 0.50
COURT_MIDCOURT_MARGIN_Y = 0.05
COURT_Y_CONVENTION = "court_y_low_near_high_far_v024"
DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE = 0.18
DEFAULT_HIT_PLAYER_REVIEW_DISTANCE_MAX_TEMPLATE = 0.33
DEFAULT_HIT_NEAR_PLAYER_DIRECTION_DELTA_DEGREES = 15.0
DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE = 0.015
DEFAULT_HIT_MIN_SPEED_DELTA_FRACTION = 0.10
DEFAULT_HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION = 0.45
DEFAULT_HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES = 5.0
DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE = 0.18
DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES = 25.0
DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES = 20.0
DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS = 2.0
DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION = 0.05
DEFAULT_BOUNCE_FALLBACK_ENABLED = True
DEFAULT_BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION = 0.35
DEFAULT_CANDIDATE_DEDUPE_MS = 500
DEFAULT_PLAYER_TIME_WINDOW_MS = 300
DEFAULT_BOUNCE_TEMPLATE_MARGIN = 0.08
DEFAULT_PLAYER_ANCHORED_HIT_ENABLED = True
DEFAULT_PLAYER_ANCHORED_HIT_LOOKBACK_MS = 700
DEFAULT_PLAYER_ANCHORED_HIT_LOOKAHEAD_MS = 1300
DEFAULT_PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE = 0.24
DEFAULT_PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE = 0.015
DEFAULT_PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS = 60
DEFAULT_EVENT_OVERLAP_DISTANCE_TEMPLATE = 0.08
DEFAULT_NET_AXIS_REVERSAL_HIT_ENABLED = True
DEFAULT_NET_AXIS_REVERSAL_LOOKBACK_MS = 700
DEFAULT_NET_AXIS_REVERSAL_LOOKAHEAD_MS = 700
DEFAULT_NET_AXIS_REVERSAL_MIN_DELTA_TEMPLATE = 0.015
DEFAULT_NET_AXIS_REVERSAL_MIN_PRE_POST_GAP_MS = 60
DEFAULT_NET_AXIS_REVERSAL_DEDUPE_DISTANCE_TEMPLATE = 0.08
HIT_CONFIDENCE_CAP = 0.70
BOUNCE_CONFIDENCE_CAP = 0.60
EVENT_CANDIDATE_WARNINGS = {
    "candidate_only": True,
    "event_candidate_only": True,
    "not_hit_truth": True,
    "not_bounce_truth": True,
    "not_in_out_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_score_or_point_truth": True,
}


@dataclass(frozen=True)
class HitBounceCandidateConfig:
    hit_player_distance_max_template: float = DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE
    hit_player_review_distance_max_template: float = (
        DEFAULT_HIT_PLAYER_REVIEW_DISTANCE_MAX_TEMPLATE
    )
    hit_near_player_direction_delta_degrees: float = (
        DEFAULT_HIT_NEAR_PLAYER_DIRECTION_DELTA_DEGREES
    )
    hit_min_net_axis_delta_template: float = DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE
    hit_min_speed_delta_fraction: float = DEFAULT_HIT_MIN_SPEED_DELTA_FRACTION
    hit_contact_fallback_min_speed_delta_fraction: float = (
        DEFAULT_HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION
    )
    hit_contact_fallback_min_direction_delta_degrees: float = (
        DEFAULT_HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES
    )
    bounce_player_distance_min_template: float = DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE
    hit_min_direction_delta_degrees: float = DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES
    bounce_min_direction_delta_degrees: float = DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES
    bounce_min_image_y_delta_pixels: float = DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS
    bounce_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION
    )
    bounce_fallback_enabled: bool = DEFAULT_BOUNCE_FALLBACK_ENABLED
    bounce_fallback_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION
    )
    candidate_dedupe_ms: int = DEFAULT_CANDIDATE_DEDUPE_MS
    player_time_window_ms: int = DEFAULT_PLAYER_TIME_WINDOW_MS
    bounce_inside_template_margin: float = DEFAULT_BOUNCE_TEMPLATE_MARGIN
    player_anchored_hit_enabled: bool = DEFAULT_PLAYER_ANCHORED_HIT_ENABLED
    player_anchored_hit_lookback_ms: int = DEFAULT_PLAYER_ANCHORED_HIT_LOOKBACK_MS
    player_anchored_hit_lookahead_ms: int = DEFAULT_PLAYER_ANCHORED_HIT_LOOKAHEAD_MS
    player_anchored_hit_distance_max_template: float = (
        DEFAULT_PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE
    )
    player_anchored_hit_min_net_axis_delta_template: float = (
        DEFAULT_PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE
    )
    player_anchored_hit_min_pre_post_gap_ms: int = (
        DEFAULT_PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS
    )
    event_overlap_distance_template: float = DEFAULT_EVENT_OVERLAP_DISTANCE_TEMPLATE
    net_axis_reversal_hit_enabled: bool = DEFAULT_NET_AXIS_REVERSAL_HIT_ENABLED
    net_axis_reversal_lookback_ms: int = DEFAULT_NET_AXIS_REVERSAL_LOOKBACK_MS
    net_axis_reversal_lookahead_ms: int = DEFAULT_NET_AXIS_REVERSAL_LOOKAHEAD_MS
    net_axis_reversal_min_delta_template: float = (
        DEFAULT_NET_AXIS_REVERSAL_MIN_DELTA_TEMPLATE
    )
    net_axis_reversal_min_pre_post_gap_ms: int = (
        DEFAULT_NET_AXIS_REVERSAL_MIN_PRE_POST_GAP_MS
    )
    net_axis_reversal_dedupe_distance_template: float = (
        DEFAULT_NET_AXIS_REVERSAL_DEDUPE_DISTANCE_TEMPLATE
    )

    def as_dict(self) -> dict[str, float | int | bool]:
        return {
            "hit_player_distance_max_template": self.hit_player_distance_max_template,
            "hit_player_review_distance_max_template": (
                self.hit_player_review_distance_max_template
            ),
            "hit_near_player_direction_delta_degrees": (
                self.hit_near_player_direction_delta_degrees
            ),
            "hit_min_net_axis_delta_template": self.hit_min_net_axis_delta_template,
            "hit_min_speed_delta_fraction": self.hit_min_speed_delta_fraction,
            "hit_contact_fallback_min_speed_delta_fraction": (
                self.hit_contact_fallback_min_speed_delta_fraction
            ),
            "hit_contact_fallback_min_direction_delta_degrees": (
                self.hit_contact_fallback_min_direction_delta_degrees
            ),
            "bounce_player_distance_min_template": self.bounce_player_distance_min_template,
            "hit_min_direction_delta_degrees": self.hit_min_direction_delta_degrees,
            "bounce_min_direction_delta_degrees": self.bounce_min_direction_delta_degrees,
            "bounce_min_image_y_delta_pixels": self.bounce_min_image_y_delta_pixels,
            "bounce_min_speed_reduction_fraction": (
                self.bounce_min_speed_reduction_fraction
            ),
            "bounce_fallback_enabled": self.bounce_fallback_enabled,
            "bounce_fallback_min_speed_reduction_fraction": (
                self.bounce_fallback_min_speed_reduction_fraction
            ),
            "candidate_dedupe_ms": self.candidate_dedupe_ms,
            "player_time_window_ms": self.player_time_window_ms,
            "bounce_inside_template_margin": self.bounce_inside_template_margin,
            "player_anchored_hit_enabled": self.player_anchored_hit_enabled,
            "player_anchored_hit_lookback_ms": self.player_anchored_hit_lookback_ms,
            "player_anchored_hit_lookahead_ms": self.player_anchored_hit_lookahead_ms,
            "player_anchored_hit_distance_max_template": (
                self.player_anchored_hit_distance_max_template
            ),
            "player_anchored_hit_min_net_axis_delta_template": (
                self.player_anchored_hit_min_net_axis_delta_template
            ),
            "player_anchored_hit_min_pre_post_gap_ms": (
                self.player_anchored_hit_min_pre_post_gap_ms
            ),
            "event_overlap_distance_template": self.event_overlap_distance_template,
            "net_axis_reversal_hit_enabled": self.net_axis_reversal_hit_enabled,
            "net_axis_reversal_lookback_ms": self.net_axis_reversal_lookback_ms,
            "net_axis_reversal_lookahead_ms": self.net_axis_reversal_lookahead_ms,
            "net_axis_reversal_min_delta_template": (
                self.net_axis_reversal_min_delta_template
            ),
            "net_axis_reversal_min_pre_post_gap_ms": (
                self.net_axis_reversal_min_pre_post_gap_ms
            ),
            "net_axis_reversal_dedupe_distance_template": (
                self.net_axis_reversal_dedupe_distance_template
            ),
        }


@dataclass(frozen=True)
class TrajectoryPoint:
    trajectory_observation: Observation
    frame_number: int
    timestamp_ms: int
    court_x: float
    court_y: float
    source_ball_court_projection_observation_id: str | None
    source_homography_observation_id: str | None
    homography_time_delta_ms: int | None
    homography_carried_forward: bool
    inside_template_bounds: bool
    image_x: float | None = None
    image_y: float | None = None


@dataclass(frozen=True)
class TrajectoryContext:
    previous: TrajectoryPoint
    current: TrajectoryPoint
    next: TrajectoryPoint
    direction_before_degrees: float
    direction_after_degrees: float
    direction_delta_degrees: float
    speed_before: float
    speed_after: float
    speed_delta_fraction: float


@dataclass(frozen=True)
class PlayerProjection:
    observation: Observation
    frame_number: int
    timestamp_ms: int
    court_x: float
    court_y: float
    track_candidate_id: str | None
    track_role_candidate: str | None
    image_x: float | None = None
    image_y: float | None = None


@dataclass(frozen=True)
class NearestPlayerContext:
    player: PlayerProjection
    distance_template_units: float
    time_delta_ms: int


@dataclass(frozen=True)
class EventCandidateDraft:
    observation_type: Literal["hit_candidate", "bounce_candidate"]
    candidate_method: str
    trajectory_context: TrajectoryContext
    nearest_player: NearestPlayerContext | None
    reason_codes: list[str]
    confidence: float
    player_proximity_gate: dict[str, Any]
    candidate_decision: dict[str, Any]
    net_axis_reversal: dict[str, Any] | None = None
    vertical_motion_proxy: dict[str, Any] | None = None
    speed_reduction: dict[str, Any] | None = None
    original_observation_type: Literal["hit_candidate", "bounce_candidate"] | None = None
    original_candidate_method: str | None = None
    court_side_zone: dict[str, Any] | None = None
    player_contact_zone: dict[str, Any] | None = None
    court_landing_zone: dict[str, Any] | None = None
    candidate_reclassification: dict[str, Any] | None = None
    candidate_sequence: dict[str, Any] | None = None
    player_anchored_hit_recall: dict[str, Any] | None = None
    player_anchor_contact_zone: dict[str, Any] | None = None
    net_axis_reversal_recall: dict[str, Any] | None = None
    overlap_suppression: dict[str, Any] | None = None

    @property
    def timestamp_ms(self) -> int:
        return self.trajectory_context.current.timestamp_ms

    @property
    def frame_number(self) -> int:
        return self.trajectory_context.current.frame_number


@dataclass(frozen=True)
class EventCandidateRejectionDiagnostic:
    trajectory_context: TrajectoryContext
    nearest_player: NearestPlayerContext | None
    net_axis_reversal: dict[str, Any]
    vertical_motion_proxy: dict[str, Any]
    speed_reduction: dict[str, Any]
    player_proximity_gate: dict[str, Any]
    candidate_decision: dict[str, Any]
    rejection_reasons: list[str]
    inside_or_near_court_template: bool
    diagnostic_source: str = "local_trajectory_context"
    player_anchored_hit_recall: dict[str, Any] | None = None
    player_anchor_contact_zone: dict[str, Any] | None = None
    net_axis_reversal_recall: dict[str, Any] | None = None
    overlap_suppression: dict[str, Any] | None = None

    @property
    def timestamp_ms(self) -> int:
        return self.trajectory_context.current.timestamp_ms

    @property
    def frame_number(self) -> int:
        return self.trajectory_context.current.frame_number


def build_hit_bounce_candidates_plan(
    *,
    media_id: str = "<media_id>",
    ball_trajectory_run_id: str = "<ball_trajectory_run_id>",
    court_projection_run_id: str = "<court_projection_run_id>",
    run_name: str = "hit-bounce-candidate-evidence-v0",
    hit_player_distance_max_template: float = DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE,
    bounce_player_distance_min_template: float = DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE,
    hit_min_direction_delta_degrees: float = DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES,
    bounce_min_direction_delta_degrees: float = DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES,
    hit_min_net_axis_delta_template: float = DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE,
    bounce_min_image_y_delta_pixels: float = DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS,
    bounce_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION
    ),
    hit_player_time_window_ms: int = DEFAULT_PLAYER_TIME_WINDOW_MS,
    hit_contact_fallback_min_speed_delta_fraction: float = (
        DEFAULT_HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION
    ),
    hit_contact_fallback_min_direction_delta_degrees: float = (
        DEFAULT_HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES
    ),
    bounce_fallback_enabled: bool = DEFAULT_BOUNCE_FALLBACK_ENABLED,
    bounce_fallback_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION
    ),
    candidate_dedupe_ms: int = DEFAULT_CANDIDATE_DEDUPE_MS,
    player_anchored_hit_enabled: bool = DEFAULT_PLAYER_ANCHORED_HIT_ENABLED,
    player_anchored_hit_lookback_ms: int = DEFAULT_PLAYER_ANCHORED_HIT_LOOKBACK_MS,
    player_anchored_hit_lookahead_ms: int = DEFAULT_PLAYER_ANCHORED_HIT_LOOKAHEAD_MS,
    player_anchored_hit_distance_max_template: float = (
        DEFAULT_PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE
    ),
    player_anchored_hit_min_net_axis_delta_template: float = (
        DEFAULT_PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE
    ),
    player_anchored_hit_min_pre_post_gap_ms: int = (
        DEFAULT_PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS
    ),
    event_overlap_distance_template: float = DEFAULT_EVENT_OVERLAP_DISTANCE_TEMPLATE,
    net_axis_reversal_hit_enabled: bool = DEFAULT_NET_AXIS_REVERSAL_HIT_ENABLED,
    net_axis_reversal_lookback_ms: int = DEFAULT_NET_AXIS_REVERSAL_LOOKBACK_MS,
    net_axis_reversal_lookahead_ms: int = DEFAULT_NET_AXIS_REVERSAL_LOOKAHEAD_MS,
    net_axis_reversal_min_delta_template: float = (
        DEFAULT_NET_AXIS_REVERSAL_MIN_DELTA_TEMPLATE
    ),
    net_axis_reversal_min_pre_post_gap_ms: int = (
        DEFAULT_NET_AXIS_REVERSAL_MIN_PRE_POST_GAP_MS
    ),
    net_axis_reversal_dedupe_distance_template: float = (
        DEFAULT_NET_AXIS_REVERSAL_DEDUPE_DISTANCE_TEMPLATE
    ),
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    bounce_fallback_cli_flag = (
        "--bounce-fallback-enabled"
        if bounce_fallback_enabled
        else "--no-bounce-fallback-enabled"
    )
    player_anchor_cli_flag = (
        "--player-anchored-hit-enabled"
        if player_anchored_hit_enabled
        else "--no-player-anchored-hit-enabled"
    )
    net_axis_reversal_cli_flag = (
        "--net-axis-reversal-hit-enabled"
        if net_axis_reversal_hit_enabled
        else "--no-net-axis-reversal-hit-enabled"
    )
    return {
        "steps": [
            "validate_media_and_source_runs",
            "load_ball_trajectory_court_candidates",
            "load_main_player_court_projection_candidates",
            "load_source_ball_projection_image_points",
            "evaluate_net_axis_reversal_vertical_proxy_speed_and_player_proximity",
            "evaluate_ball_first_net_axis_reversal_hit_recall",
            "evaluate_player_anchored_hit_recall",
            "dedupe_candidate_clusters",
            "apply_side_zone_sequence_classification_prior",
            "persist_hit_and_bounce_candidate_observations",
            "write_candidate_source_lineage",
        ],
        "command": (
            "python -m apps.worker.cli build-hit-bounce-candidates "
            f"--media-id {media_id} "
            f"--ball-trajectory-run-id {ball_trajectory_run_id} "
            f"--court-projection-run-id {court_projection_run_id} "
            f"--run-name {run_name} "
            f"--hit-player-distance-max-template {hit_player_distance_max_template} "
            f"--bounce-player-distance-min-template {bounce_player_distance_min_template} "
            f"--hit-min-direction-delta-degrees {hit_min_direction_delta_degrees} "
            f"--bounce-min-direction-delta-degrees {bounce_min_direction_delta_degrees} "
            f"--hit-min-net-axis-delta-template {hit_min_net_axis_delta_template} "
            f"--bounce-min-image-y-delta-pixels {bounce_min_image_y_delta_pixels} "
            f"--bounce-min-speed-reduction-fraction {bounce_min_speed_reduction_fraction} "
            f"--hit-player-time-window-ms {hit_player_time_window_ms} "
            "--hit-contact-fallback-min-speed-delta-fraction "
            f"{hit_contact_fallback_min_speed_delta_fraction} "
            "--hit-contact-fallback-min-direction-delta-degrees "
            f"{hit_contact_fallback_min_direction_delta_degrees} "
            f"{bounce_fallback_cli_flag} "
            "--bounce-fallback-min-speed-reduction-fraction "
            f"{bounce_fallback_min_speed_reduction_fraction} "
            f"{player_anchor_cli_flag} "
            "--player-anchored-hit-lookback-ms "
            f"{player_anchored_hit_lookback_ms} "
            "--player-anchored-hit-lookahead-ms "
            f"{player_anchored_hit_lookahead_ms} "
            "--player-anchored-hit-distance-max-template "
            f"{player_anchored_hit_distance_max_template} "
            "--player-anchored-hit-min-net-axis-delta-template "
            f"{player_anchored_hit_min_net_axis_delta_template} "
            "--player-anchored-hit-min-pre-post-gap-ms "
            f"{player_anchored_hit_min_pre_post_gap_ms} "
            "--event-overlap-distance-template "
            f"{event_overlap_distance_template} "
            f"{net_axis_reversal_cli_flag} "
            "--net-axis-reversal-lookback-ms "
            f"{net_axis_reversal_lookback_ms} "
            "--net-axis-reversal-lookahead-ms "
            f"{net_axis_reversal_lookahead_ms} "
            "--net-axis-reversal-min-delta-template "
            f"{net_axis_reversal_min_delta_template} "
            "--net-axis-reversal-min-pre-post-gap-ms "
            f"{net_axis_reversal_min_pre_post_gap_ms} "
            "--net-axis-reversal-dedupe-distance-template "
            f"{net_axis_reversal_dedupe_distance_template} "
            f"--candidate-dedupe-ms {candidate_dedupe_ms}"
        ),
        "run_name": run_name,
        "source_run_ids": {
            "ball_trajectory_run_id": ball_trajectory_run_id,
            "court_projection_run_id": court_projection_run_id,
        },
        "candidate_method": EVENT_CANDIDATE_METHOD,
        "hit_candidate_method": HIT_CANDIDATE_METHOD,
        "net_axis_reversal_hit_candidate_method": (
            NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
        ),
        "player_anchored_hit_candidate_method": PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
        "bounce_candidate_method": BOUNCE_CANDIDATE_METHOD,
        "classification_priority": "side_zone_sequence_candidate_prior",
        "court_y_convention": COURT_Y_CONVENTION,
        "coordinate_space": CoordinateSpace.court_template_2d,
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "thresholds": {
            "hit_player_distance_max_template": hit_player_distance_max_template,
            "hit_player_review_distance_max_template": (
                DEFAULT_HIT_PLAYER_REVIEW_DISTANCE_MAX_TEMPLATE
            ),
            "hit_near_player_direction_delta_degrees": (
                DEFAULT_HIT_NEAR_PLAYER_DIRECTION_DELTA_DEGREES
            ),
            "hit_min_net_axis_delta_template": hit_min_net_axis_delta_template,
            "hit_min_speed_delta_fraction": DEFAULT_HIT_MIN_SPEED_DELTA_FRACTION,
            "hit_contact_fallback_min_speed_delta_fraction": (
                hit_contact_fallback_min_speed_delta_fraction
            ),
            "hit_contact_fallback_min_direction_delta_degrees": (
                hit_contact_fallback_min_direction_delta_degrees
            ),
            "bounce_player_distance_min_template": bounce_player_distance_min_template,
            "hit_min_direction_delta_degrees": hit_min_direction_delta_degrees,
            "bounce_min_direction_delta_degrees": bounce_min_direction_delta_degrees,
            "bounce_min_image_y_delta_pixels": bounce_min_image_y_delta_pixels,
            "bounce_min_speed_reduction_fraction": bounce_min_speed_reduction_fraction,
            "bounce_fallback_enabled": bounce_fallback_enabled,
            "bounce_fallback_min_speed_reduction_fraction": (
                bounce_fallback_min_speed_reduction_fraction
            ),
            "player_time_window_ms": hit_player_time_window_ms,
            "candidate_dedupe_ms": candidate_dedupe_ms,
            "player_anchored_hit_enabled": player_anchored_hit_enabled,
            "player_anchored_hit_lookback_ms": player_anchored_hit_lookback_ms,
            "player_anchored_hit_lookahead_ms": player_anchored_hit_lookahead_ms,
            "player_anchored_hit_distance_max_template": (
                player_anchored_hit_distance_max_template
            ),
            "player_anchored_hit_min_net_axis_delta_template": (
                player_anchored_hit_min_net_axis_delta_template
            ),
            "player_anchored_hit_min_pre_post_gap_ms": (
                player_anchored_hit_min_pre_post_gap_ms
            ),
            "event_overlap_distance_template": event_overlap_distance_template,
            "net_axis_reversal_hit_enabled": net_axis_reversal_hit_enabled,
            "net_axis_reversal_lookback_ms": net_axis_reversal_lookback_ms,
            "net_axis_reversal_lookahead_ms": net_axis_reversal_lookahead_ms,
            "net_axis_reversal_min_delta_template": (
                net_axis_reversal_min_delta_template
            ),
            "net_axis_reversal_min_pre_post_gap_ms": (
                net_axis_reversal_min_pre_post_gap_ms
            ),
            "net_axis_reversal_dedupe_distance_template": (
                net_axis_reversal_dedupe_distance_template
            ),
        },
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
            f"?courtProjectionRunId={court_projection_run_id}"
            f"&ballTrajectoryRunId={ball_trajectory_run_id}"
            "&eventCandidateRunId=<event_candidate_run_id>"
        ),
        "warnings": dict(EVENT_CANDIDATE_WARNINGS),
    }


def build_hit_bounce_candidates(
    *,
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    run_name: str = "hit-bounce-candidate-evidence-v0",
    hit_player_distance_max_template: float = DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE,
    bounce_player_distance_min_template: float = DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE,
    hit_min_direction_delta_degrees: float = DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES,
    bounce_min_direction_delta_degrees: float = DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES,
    hit_min_net_axis_delta_template: float = DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE,
    bounce_min_image_y_delta_pixels: float = DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS,
    bounce_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION
    ),
    hit_player_time_window_ms: int = DEFAULT_PLAYER_TIME_WINDOW_MS,
    hit_contact_fallback_min_speed_delta_fraction: float = (
        DEFAULT_HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION
    ),
    hit_contact_fallback_min_direction_delta_degrees: float = (
        DEFAULT_HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES
    ),
    bounce_fallback_enabled: bool = DEFAULT_BOUNCE_FALLBACK_ENABLED,
    bounce_fallback_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION
    ),
    candidate_dedupe_ms: int = DEFAULT_CANDIDATE_DEDUPE_MS,
    player_anchored_hit_enabled: bool = DEFAULT_PLAYER_ANCHORED_HIT_ENABLED,
    player_anchored_hit_lookback_ms: int = DEFAULT_PLAYER_ANCHORED_HIT_LOOKBACK_MS,
    player_anchored_hit_lookahead_ms: int = DEFAULT_PLAYER_ANCHORED_HIT_LOOKAHEAD_MS,
    player_anchored_hit_distance_max_template: float = (
        DEFAULT_PLAYER_ANCHORED_HIT_DISTANCE_MAX_TEMPLATE
    ),
    player_anchored_hit_min_net_axis_delta_template: float = (
        DEFAULT_PLAYER_ANCHORED_HIT_MIN_NET_AXIS_DELTA_TEMPLATE
    ),
    player_anchored_hit_min_pre_post_gap_ms: int = (
        DEFAULT_PLAYER_ANCHORED_HIT_MIN_PRE_POST_GAP_MS
    ),
    event_overlap_distance_template: float = DEFAULT_EVENT_OVERLAP_DISTANCE_TEMPLATE,
    net_axis_reversal_hit_enabled: bool = DEFAULT_NET_AXIS_REVERSAL_HIT_ENABLED,
    net_axis_reversal_lookback_ms: int = DEFAULT_NET_AXIS_REVERSAL_LOOKBACK_MS,
    net_axis_reversal_lookahead_ms: int = DEFAULT_NET_AXIS_REVERSAL_LOOKAHEAD_MS,
    net_axis_reversal_min_delta_template: float = (
        DEFAULT_NET_AXIS_REVERSAL_MIN_DELTA_TEMPLATE
    ),
    net_axis_reversal_min_pre_post_gap_ms: int = (
        DEFAULT_NET_AXIS_REVERSAL_MIN_PRE_POST_GAP_MS
    ),
    net_axis_reversal_dedupe_distance_template: float = (
        DEFAULT_NET_AXIS_REVERSAL_DEDUPE_DISTANCE_TEMPLATE
    ),
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    config = HitBounceCandidateConfig(
        hit_player_distance_max_template=hit_player_distance_max_template,
        bounce_player_distance_min_template=bounce_player_distance_min_template,
        hit_min_direction_delta_degrees=hit_min_direction_delta_degrees,
        bounce_min_direction_delta_degrees=bounce_min_direction_delta_degrees,
        hit_min_net_axis_delta_template=hit_min_net_axis_delta_template,
        hit_contact_fallback_min_speed_delta_fraction=(
            hit_contact_fallback_min_speed_delta_fraction
        ),
        hit_contact_fallback_min_direction_delta_degrees=(
            hit_contact_fallback_min_direction_delta_degrees
        ),
        bounce_min_image_y_delta_pixels=bounce_min_image_y_delta_pixels,
        bounce_min_speed_reduction_fraction=bounce_min_speed_reduction_fraction,
        bounce_fallback_enabled=bounce_fallback_enabled,
        bounce_fallback_min_speed_reduction_fraction=(
            bounce_fallback_min_speed_reduction_fraction
        ),
        candidate_dedupe_ms=candidate_dedupe_ms,
        player_time_window_ms=hit_player_time_window_ms,
        player_anchored_hit_enabled=player_anchored_hit_enabled,
        player_anchored_hit_lookback_ms=player_anchored_hit_lookback_ms,
        player_anchored_hit_lookahead_ms=player_anchored_hit_lookahead_ms,
        player_anchored_hit_distance_max_template=(
            player_anchored_hit_distance_max_template
        ),
        player_anchored_hit_min_net_axis_delta_template=(
            player_anchored_hit_min_net_axis_delta_template
        ),
        player_anchored_hit_min_pre_post_gap_ms=(
            player_anchored_hit_min_pre_post_gap_ms
        ),
        event_overlap_distance_template=event_overlap_distance_template,
        net_axis_reversal_hit_enabled=net_axis_reversal_hit_enabled,
        net_axis_reversal_lookback_ms=net_axis_reversal_lookback_ms,
        net_axis_reversal_lookahead_ms=net_axis_reversal_lookahead_ms,
        net_axis_reversal_min_delta_template=net_axis_reversal_min_delta_template,
        net_axis_reversal_min_pre_post_gap_ms=net_axis_reversal_min_pre_post_gap_ms,
        net_axis_reversal_dedupe_distance_template=(
            net_axis_reversal_dedupe_distance_template
        ),
    )
    invalid = _validate_config(config)
    if invalid is not None:
        return invalid
    plan = build_hit_bounce_candidates_plan(
        media_id=media_id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        court_projection_run_id=court_projection_run_id,
        run_name=run_name,
        hit_player_distance_max_template=hit_player_distance_max_template,
        bounce_player_distance_min_template=bounce_player_distance_min_template,
        hit_min_direction_delta_degrees=hit_min_direction_delta_degrees,
        bounce_min_direction_delta_degrees=bounce_min_direction_delta_degrees,
        hit_min_net_axis_delta_template=hit_min_net_axis_delta_template,
        bounce_min_image_y_delta_pixels=bounce_min_image_y_delta_pixels,
        bounce_min_speed_reduction_fraction=bounce_min_speed_reduction_fraction,
        hit_player_time_window_ms=hit_player_time_window_ms,
        hit_contact_fallback_min_speed_delta_fraction=(
            hit_contact_fallback_min_speed_delta_fraction
        ),
        hit_contact_fallback_min_direction_delta_degrees=(
            hit_contact_fallback_min_direction_delta_degrees
        ),
        bounce_fallback_enabled=bounce_fallback_enabled,
        bounce_fallback_min_speed_reduction_fraction=(
            bounce_fallback_min_speed_reduction_fraction
        ),
        candidate_dedupe_ms=candidate_dedupe_ms,
        player_anchored_hit_enabled=player_anchored_hit_enabled,
        player_anchored_hit_lookback_ms=player_anchored_hit_lookback_ms,
        player_anchored_hit_lookahead_ms=player_anchored_hit_lookahead_ms,
        player_anchored_hit_distance_max_template=(
            player_anchored_hit_distance_max_template
        ),
        player_anchored_hit_min_net_axis_delta_template=(
            player_anchored_hit_min_net_axis_delta_template
        ),
        player_anchored_hit_min_pre_post_gap_ms=(
            player_anchored_hit_min_pre_post_gap_ms
        ),
        event_overlap_distance_template=event_overlap_distance_template,
        net_axis_reversal_hit_enabled=net_axis_reversal_hit_enabled,
        net_axis_reversal_lookback_ms=net_axis_reversal_lookback_ms,
        net_axis_reversal_lookahead_ms=net_axis_reversal_lookahead_ms,
        net_axis_reversal_min_delta_template=net_axis_reversal_min_delta_template,
        net_axis_reversal_min_pre_post_gap_ms=net_axis_reversal_min_pre_post_gap_ms,
        net_axis_reversal_dedupe_distance_template=(
            net_axis_reversal_dedupe_distance_template
        ),
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "hit/bounce candidate evidence build planned",
            "plan": plan,
            "warnings": dict(EVENT_CANDIDATE_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")
    for label, run_id in (
        ("ball_trajectory_run_id", ball_trajectory_run_id),
        ("court_projection_run_id", court_projection_run_id),
    ):
        source_run = session.get(ProcessingRun, run_id)
        if source_run is None:
            return _failed(f"missing_{label}", f"source run not found: {run_id}")
        if source_run.media_id != media.id:
            return _failed(f"{label}_media_mismatch", f"{label} does not match media_id")

    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            config=config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            config=config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        trajectory_segments = load_ball_trajectory_segments(
            session=session,
            media=media,
            ball_trajectory_run_id=ball_trajectory_run_id,
        )
        player_projections = load_main_player_court_projections(
            session=session,
            media=media,
            court_projection_run_id=court_projection_run_id,
        )
        (
            evaluated_contexts,
            hit_drafts,
            bounce_drafts,
            rejection_diagnostics,
        ) = evaluate_event_candidates(
            trajectory_segments=trajectory_segments,
            player_projections=player_projections,
            config=config,
        )
        (
            net_axis_reversal_context_count,
            net_axis_reversal_hit_drafts,
            net_axis_reversal_rejection_diagnostics,
        ) = evaluate_net_axis_reversal_hit_recall(
            trajectory_segments=trajectory_segments,
            player_projections=player_projections,
            config=config,
        )
        hit_drafts.extend(net_axis_reversal_hit_drafts)
        rejection_diagnostics.extend(net_axis_reversal_rejection_diagnostics)
        (
            player_anchor_context_count,
            player_anchored_hit_drafts,
            player_anchored_rejection_diagnostics,
        ) = evaluate_player_anchored_hit_recall(
            trajectory_segments=trajectory_segments,
            player_projections=player_projections,
            config=config,
        )
        hit_drafts.extend(player_anchored_hit_drafts)
        rejection_diagnostics.extend(player_anchored_rejection_diagnostics)
        deduped_hits, deduped_hit_rejections = dedupe_event_candidates_with_rejections(
            hit_drafts,
            candidate_dedupe_ms=config.candidate_dedupe_ms,
        )
        deduped_bounces, deduped_bounce_rejections = (
            dedupe_event_candidates_with_rejections(
                bounce_drafts,
                candidate_dedupe_ms=config.candidate_dedupe_ms,
            )
        )
        (
            deduped_bounces,
            suppressed_bounce_conflict_count,
            suppressed_bounce_rejections,
        ) = suppress_bounces_near_hits(
            deduped_hits,
            deduped_bounces,
            candidate_dedupe_ms=config.candidate_dedupe_ms,
        )
        rejection_diagnostics.extend(deduped_hit_rejections)
        rejection_diagnostics.extend(deduped_bounce_rejections)
        rejection_diagnostics.extend(suppressed_bounce_rejections)
        (
            final_candidates,
            sequence_reclassification_summary,
        ) = apply_side_zone_sequence_classification(
            [*deduped_hits, *deduped_bounces],
            config=config,
        )
        (
            final_candidates,
            net_axis_overlap_suppressed_count,
            net_axis_overlap_rejections,
        ) = suppress_weak_net_axis_reversal_hits_overlapping_bounces(
            final_candidates,
            config=config,
        )
        rejection_diagnostics.extend(net_axis_overlap_rejections)
        (
            final_candidates,
            player_anchor_suppressed_overlap_count,
            player_anchor_overlap_rejections,
        ) = suppress_player_anchored_hits_overlapping_bounces(
            final_candidates,
            config=config,
        )
        rejection_diagnostics.extend(player_anchor_overlap_rejections)
        writer = ObservationWriter(session)
        observations = _persist_event_candidates_and_diagnostics(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            candidates=final_candidates,
            diagnostics=rejection_diagnostics,
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session=session, run=run, step=step, message=str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    counts = Counter(row.observation_type for row in observations)
    candidate_summary = {
        "trajectory_segment_count": len(trajectory_segments),
        "evaluated_trajectory_points": evaluated_contexts,
        "hit_candidate_count": len(hit_drafts),
        "bounce_candidate_count": len(bounce_drafts),
        "raw_hit_candidate_count": len(hit_drafts),
        "raw_bounce_candidate_count": len(bounce_drafts),
        "deduped_hit_candidate_count": len(deduped_hits),
        "deduped_bounce_candidate_count": len(deduped_bounces),
        "final_hit_candidate_count": sum(
            1
            for candidate in final_candidates
            if candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
        ),
        "final_bounce_candidate_count": sum(
            1
            for candidate in final_candidates
            if candidate.observation_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE
        ),
        **sequence_reclassification_summary,
        "suppressed_bounce_conflict_count": suppressed_bounce_conflict_count,
        "rejected_context_count": len(rejection_diagnostics),
        "rejection_reasons": _rejection_reason_counts(rejection_diagnostics),
        "diagnostic_observation_count": counts.get(
            EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE,
            0,
        ),
        "classification_priority": "side_zone_sequence_candidate_prior",
        "physics_heuristic_version": "v0.2.5",
        "contact_zone_tightening_version": "v0.2.4",
        "net_axis_reversal_hit_recall_version": "v0.2.5",
        "net_axis_reversal_context_count": net_axis_reversal_context_count,
        "net_axis_reversal_candidate_count": len(net_axis_reversal_hit_drafts),
        "net_axis_reversal_recovered_hit_count": sum(
            1
            for candidate in final_candidates
            if (
                candidate.original_candidate_method
                or candidate.candidate_method
            )
            == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
            and candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
        ),
        "net_axis_reversal_suppressed_overlap_count": (
            net_axis_overlap_suppressed_count
        ),
        "net_axis_reversal_rejected_count": (
            len(net_axis_reversal_rejection_diagnostics)
            + len(net_axis_overlap_rejections)
        ),
        "net_axis_reversal_rejection_reasons": _rejection_reason_counts(
            [*net_axis_reversal_rejection_diagnostics, *net_axis_overlap_rejections]
        ),
        "net_axis_reversal_hit_recall": {
            "enabled": config.net_axis_reversal_hit_enabled,
            "reversal_context_count": net_axis_reversal_context_count,
            "reversal_candidate_count": len(net_axis_reversal_hit_drafts),
            "reversal_recovered_hit_count": sum(
                1
                for candidate in final_candidates
                if (
                    candidate.original_candidate_method
                    or candidate.candidate_method
                )
                == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
                and candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
            ),
            "reversal_suppressed_overlap_count": net_axis_overlap_suppressed_count,
            "reversal_rejected_count": (
                len(net_axis_reversal_rejection_diagnostics)
                + len(net_axis_overlap_rejections)
            ),
            "rejection_reasons": _rejection_reason_counts(
                [*net_axis_reversal_rejection_diagnostics, *net_axis_overlap_rejections]
            ),
            "player_proximity_required": False,
        },
        "player_anchor_context_count": player_anchor_context_count,
        "player_anchor_candidate_count": len(player_anchored_hit_drafts),
        "player_anchor_recovered_hit_count": sum(
            1
            for candidate in final_candidates
            if (
                candidate.original_candidate_method
                or candidate.candidate_method
            )
            == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
            and candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
        ),
        "player_anchor_suppressed_overlap_count": (
            player_anchor_suppressed_overlap_count
        ),
        "player_anchor_rejected_count": (
            len(player_anchored_rejection_diagnostics)
            + len(player_anchor_overlap_rejections)
        ),
        "player_anchor_rejection_reasons": _rejection_reason_counts(
            [*player_anchored_rejection_diagnostics, *player_anchor_overlap_rejections]
        ),
        "player_anchored_hit_recall": {
            "enabled": config.player_anchored_hit_enabled,
            "player_anchor_context_count": player_anchor_context_count,
            "player_anchor_candidate_count": len(player_anchored_hit_drafts),
            "player_anchor_recovered_hit_count": sum(
                1
                for candidate in final_candidates
                if (
                    candidate.original_candidate_method
                    or candidate.candidate_method
                )
                == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
                and candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
            ),
            "player_anchor_suppressed_overlap_count": (
                player_anchor_suppressed_overlap_count
            ),
            "player_anchor_rejected_count": (
                len(player_anchored_rejection_diagnostics)
                + len(player_anchor_overlap_rejections)
            ),
            "rejection_reasons": _rejection_reason_counts(
                [*player_anchored_rejection_diagnostics, *player_anchor_overlap_rejections]
            ),
        },
    }
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_counts={
            BALL_TRAJECTORY_OBSERVATION_TYPE: len(trajectory_segments),
            MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE: len(player_projections),
        },
        output_counts=dict(counts),
        candidate_summary=candidate_summary,
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "hit/bounce candidate evidence build complete",
        "event_candidate_run_id": run.id,
        "run_id": run.id,
        "media_id": media.id,
        "source_run_ids": {
            "ball_trajectory_run_id": ball_trajectory_run_id,
            "court_projection_run_id": court_projection_run_id,
        },
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            HIT_CANDIDATE_OBSERVATION_TYPE: counts.get(HIT_CANDIDATE_OBSERVATION_TYPE, 0),
            BOUNCE_CANDIDATE_OBSERVATION_TYPE: counts.get(
                BOUNCE_CANDIDATE_OBSERVATION_TYPE, 0
            ),
            EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE: counts.get(
                EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE,
                0,
            ),
            "total": sum(counts.values()),
        },
        "candidate_summary": candidate_summary,
        "observation_ids": [row.id for row in observations],
        "replay_url": (
            f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
            f"?courtProjectionRunId={court_projection_run_id}"
            f"&ballTrajectoryRunId={ball_trajectory_run_id}"
            f"&eventCandidateRunId={run.id}"
        ),
        "warnings": dict(EVENT_CANDIDATE_WARNINGS),
    }


def load_ball_trajectory_segments(
    *,
    session: Session,
    media: MediaAsset,
    ball_trajectory_run_id: str,
) -> list[list[TrajectoryPoint]]:
    rows = list(
        session.scalars(
            select(Observation)
            .where(
                Observation.media_id == media.id,
                Observation.run_id == ball_trajectory_run_id,
                Observation.observation_type == BALL_TRAJECTORY_OBSERVATION_TYPE,
                Observation.timestamp_start_ms.is_not(None),
            )
            .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
        ).all()
    )
    image_points_by_observation_id = _load_source_ball_projection_image_points(
        session=session,
        media=media,
        trajectory_rows=rows,
    )
    segments = []
    for row in rows:
        points = _trajectory_points_from_observation(
            row,
            image_points_by_observation_id=image_points_by_observation_id,
        )
        if points:
            segments.append(points)
    return segments


def _load_source_ball_projection_image_points(
    *,
    session: Session,
    media: MediaAsset,
    trajectory_rows: list[Observation],
) -> dict[str, tuple[float, float]]:
    source_ids: set[str] = set()
    for row in trajectory_rows:
        payload = row.payload_jsonb or {}
        raw_points = payload.get("points")
        if not isinstance(raw_points, list):
            continue
        for raw_point in raw_points:
            if not isinstance(raw_point, dict):
                continue
            source_id = _string_or_none(
                raw_point.get("source_observation_id")
                or raw_point.get("source_ball_court_projection_observation_id")
            )
            if source_id is not None:
                source_ids.add(source_id)
    if not source_ids:
        return {}
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.id.in_(source_ids),
            Observation.observation_type == BALL_COURT_PROJECTION_OBSERVATION_TYPE,
        )
    ).all()
    image_points: dict[str, tuple[float, float]] = {}
    for row in rows:
        image_point = _image_point_tuple((row.payload_jsonb or {}).get("image_point"))
        if image_point is not None:
            image_points[row.id] = image_point
    return image_points


def load_main_player_court_projections(
    *,
    session: Session,
    media: MediaAsset,
    court_projection_run_id: str,
) -> list[PlayerProjection]:
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == court_projection_run_id,
            Observation.observation_type == MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE,
            Observation.timestamp_start_ms.is_not(None),
        )
        .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
    ).all()
    projections = []
    for row in rows:
        projection = _player_projection_from_observation(row)
        if projection is not None:
            projections.append(projection)
    return projections


def evaluate_event_candidates(
    *,
    trajectory_segments: list[list[TrajectoryPoint]],
    player_projections: list[PlayerProjection],
    config: HitBounceCandidateConfig,
) -> tuple[
    int,
    list[EventCandidateDraft],
    list[EventCandidateDraft],
    list[EventCandidateRejectionDiagnostic],
]:
    hit_candidates: list[EventCandidateDraft] = []
    bounce_candidates: list[EventCandidateDraft] = []
    rejection_diagnostics: list[EventCandidateRejectionDiagnostic] = []
    evaluated_contexts = 0
    for segment in trajectory_segments:
        for index in range(1, len(segment) - 1):
            context = trajectory_context(
                segment[index - 1],
                segment[index],
                segment[index + 1],
            )
            if context is None:
                continue
            evaluated_contexts += 1
            net_axis_reversal = _net_axis_reversal_payload(segment, index, config)
            vertical_motion_proxy = _vertical_motion_proxy_payload(segment, index, config)
            speed_reduction = _speed_reduction_payload(context, config)
            nearest_player = nearest_main_player_projection(
                segment[index],
                player_projections,
                time_window_ms=config.player_time_window_ms,
            )
            hit_signal = _hit_signal_for_context(
                context,
                nearest_player,
                config,
                net_axis_reversal=net_axis_reversal,
            )
            if hit_signal is not None:
                assert nearest_player is not None
                hit_candidates.append(
                    _hit_candidate_from_context(
                        context,
                        nearest_player,
                        config,
                        net_axis_reversal=net_axis_reversal,
                        hit_signal=hit_signal,
                    )
                )
                continue
            bounce_signal = _bounce_signal_for_context(
                context,
                nearest_player,
                config,
                vertical_motion_proxy=vertical_motion_proxy,
                speed_reduction=speed_reduction,
            )
            if bounce_signal is not None:
                bounce_candidates.append(
                    _bounce_candidate_from_context(
                        context,
                        nearest_player,
                        config,
                        vertical_motion_proxy=vertical_motion_proxy,
                        speed_reduction=speed_reduction,
                        bounce_signal=bounce_signal,
                    )
                )
                continue
            rejection_diagnostics.append(
                _rejection_diagnostic_from_context(
                    context,
                    nearest_player,
                    config,
                    net_axis_reversal=net_axis_reversal,
                    vertical_motion_proxy=vertical_motion_proxy,
                    speed_reduction=speed_reduction,
                    rejection_reasons=_rejection_reasons_for_context(
                        context,
                        nearest_player,
                        config,
                        net_axis_reversal=net_axis_reversal,
                        vertical_motion_proxy=vertical_motion_proxy,
                        speed_reduction=speed_reduction,
                    ),
                )
            )
    return evaluated_contexts, hit_candidates, bounce_candidates, rejection_diagnostics


def evaluate_net_axis_reversal_hit_recall(
    *,
    trajectory_segments: list[list[TrajectoryPoint]],
    player_projections: list[PlayerProjection],
    config: HitBounceCandidateConfig,
) -> tuple[int, list[EventCandidateDraft], list[EventCandidateRejectionDiagnostic]]:
    if not config.net_axis_reversal_hit_enabled:
        return 0, [], []
    all_ball_points = _flatten_trajectory_points(trajectory_segments)
    hit_candidates: list[EventCandidateDraft] = []
    rejection_diagnostics: list[EventCandidateRejectionDiagnostic] = []
    evaluated_contexts = 0
    for anchor in all_ball_points:
        evaluated_contexts += 1
        incoming = _net_axis_reversal_incoming_point(anchor, all_ball_points, config=config)
        outgoing = _net_axis_reversal_outgoing_point(anchor, all_ball_points, config=config)
        rejection_reasons: list[str] = []
        if incoming is None:
            rejection_reasons.append("no_incoming_point_in_lookback_window")
        if outgoing is None:
            rejection_reasons.append("no_outgoing_point_in_lookahead_window")
        if rejection_reasons:
            rejection_diagnostics.append(
                _net_axis_reversal_rejection_diagnostic(
                    anchor=anchor,
                    incoming=incoming,
                    outgoing=outgoing,
                    player_projections=player_projections,
                    config=config,
                    rejection_reasons=rejection_reasons,
                )
            )
            continue
        assert incoming is not None
        assert outgoing is not None
        context = trajectory_context(incoming, anchor, outgoing)
        if context is None:
            rejection_diagnostics.append(
                _net_axis_reversal_rejection_diagnostic(
                    anchor=anchor,
                    incoming=incoming,
                    outgoing=outgoing,
                    player_projections=player_projections,
                    config=config,
                    rejection_reasons=["invalid_wide_window_context"],
                )
            )
            continue
        net_axis_reversal = _ball_first_net_axis_reversal_payload(
            incoming=incoming,
            anchor=anchor,
            outgoing=outgoing,
            player_projections=player_projections,
            config=config,
        )
        reasons: list[str] = []
        if net_axis_reversal.get("reversal") is not True:
            reasons.append("no_net_axis_reversal")
            if (
                net_axis_reversal.get("vy_before") is None
                or net_axis_reversal.get("vy_after") is None
                or abs(float(net_axis_reversal.get("vy_before") or 0.0))
                < config.net_axis_reversal_min_delta_template
                or abs(float(net_axis_reversal.get("vy_after") or 0.0))
                < config.net_axis_reversal_min_delta_template
            ):
                reasons.append("net_axis_delta_below_threshold")
        if not _inside_or_near_template(anchor, config.bounce_inside_template_margin):
            reasons.append("not_inside_or_near_court")
        if reasons:
            rejection_diagnostics.append(
                _net_axis_reversal_rejection_diagnostic(
                    anchor=anchor,
                    incoming=incoming,
                    outgoing=outgoing,
                    player_projections=player_projections,
                    config=config,
                    rejection_reasons=reasons,
                    net_axis_reversal=net_axis_reversal,
                )
            )
            continue
        nearest_player = nearest_main_player_projection(
            anchor,
            player_projections,
            time_window_ms=max(
                config.player_time_window_ms,
                config.net_axis_reversal_lookback_ms,
            ),
        )
        hit_candidates.append(
            _net_axis_reversal_hit_candidate_from_context(
                context,
                nearest_player,
                config,
                net_axis_reversal=net_axis_reversal,
            )
        )
    return evaluated_contexts, hit_candidates, rejection_diagnostics


def evaluate_player_anchored_hit_recall(
    *,
    trajectory_segments: list[list[TrajectoryPoint]],
    player_projections: list[PlayerProjection],
    config: HitBounceCandidateConfig,
) -> tuple[int, list[EventCandidateDraft], list[EventCandidateRejectionDiagnostic]]:
    if not config.player_anchored_hit_enabled:
        return 0, [], []
    all_ball_points = _flatten_trajectory_points(trajectory_segments)
    hit_candidates: list[EventCandidateDraft] = []
    rejection_diagnostics: list[EventCandidateRejectionDiagnostic] = []
    evaluated_contexts = 0
    for player in player_projections:
        if player.track_role_candidate not in {
            "near_player_track_candidate",
            "far_player_track_candidate",
        }:
            continue
        evaluated_contexts += 1
        anchor_candidates = player_anchor_ball_candidates(
            player,
            all_ball_points,
            config=config,
        )
        if not anchor_candidates:
            rejection_diagnostics.append(
                _player_anchor_rejection_diagnostic(
                    player=player,
                    anchor=None,
                    incoming=None,
                    outgoing=None,
                    config=config,
                    rejection_reasons=["no_ball_point_near_player_anchor"],
                )
            )
            continue
        accepted = False
        for anchor in anchor_candidates:
            distance = _player_anchor_distance(player, anchor)
            player_anchor_contact_zone = _player_anchor_contact_zone_payload(
                player=player,
                anchor=anchor,
                config=config,
                distance_template_units=distance,
            )
            if (
                player_anchor_contact_zone.get("side_matches_player_track")
                is not True
            ):
                rejection_diagnostics.append(
                    _player_anchor_rejection_diagnostic(
                        player=player,
                        anchor=anchor,
                        incoming=None,
                        outgoing=None,
                        config=config,
                        rejection_reasons=["side_mismatch_player_track"],
                        distance_template_units=distance,
                        player_anchor_contact_zone=player_anchor_contact_zone,
                    )
                )
                continue
            if player_anchor_contact_zone.get("in_contact_zone") is not True:
                rejection_diagnostics.append(
                    _player_anchor_rejection_diagnostic(
                        player=player,
                        anchor=anchor,
                        incoming=None,
                        outgoing=None,
                        config=config,
                        rejection_reasons=["not_player_contact_zone"],
                        distance_template_units=distance,
                        player_anchor_contact_zone=player_anchor_contact_zone,
                    )
                )
                continue
            if player_anchor_contact_zone.get("open_court_landing_zone") is True:
                rejection_diagnostics.append(
                    _player_anchor_rejection_diagnostic(
                        player=player,
                        anchor=anchor,
                        incoming=None,
                        outgoing=None,
                        config=config,
                        rejection_reasons=["open_court_landing_zone_anchor"],
                        distance_template_units=distance,
                        player_anchor_contact_zone=player_anchor_contact_zone,
                    )
                )
                continue
            incoming = _player_anchor_incoming_point(
                anchor,
                all_ball_points,
                config=config,
            )
            outgoing = _player_anchor_outgoing_point(
                anchor,
                all_ball_points,
                config=config,
            )
            rejection_reasons: list[str] = []
            if incoming is None:
                rejection_reasons.append("no_incoming_point_in_lookback_window")
            if outgoing is None:
                rejection_reasons.append("no_outgoing_point_in_lookahead_window")
            if rejection_reasons:
                rejection_diagnostics.append(
                    _player_anchor_rejection_diagnostic(
                        player=player,
                        anchor=anchor,
                        incoming=incoming,
                        outgoing=outgoing,
                        config=config,
                        rejection_reasons=rejection_reasons,
                        distance_template_units=distance,
                        player_anchor_contact_zone=player_anchor_contact_zone,
                    )
                )
                continue
            assert incoming is not None
            assert outgoing is not None
            context = trajectory_context(incoming, anchor, outgoing)
            if context is None:
                rejection_diagnostics.append(
                    _player_anchor_rejection_diagnostic(
                        player=player,
                        anchor=anchor,
                        incoming=incoming,
                        outgoing=outgoing,
                        config=config,
                        rejection_reasons=["invalid_wide_window_context"],
                        distance_template_units=distance,
                        player_anchor_contact_zone=player_anchor_contact_zone,
                    )
                )
                continue
            net_axis_reversal = _wide_window_net_axis_reversal_payload(
                incoming=incoming,
                anchor=anchor,
                outgoing=outgoing,
                config=config,
            )
            if net_axis_reversal.get("reversal") is not True:
                rejection_diagnostics.append(
                    _player_anchor_rejection_diagnostic(
                        player=player,
                        anchor=anchor,
                        incoming=incoming,
                        outgoing=outgoing,
                        config=config,
                        rejection_reasons=["no_wide_window_net_axis_reversal"],
                        distance_template_units=distance,
                        net_axis_reversal=net_axis_reversal,
                        player_anchor_contact_zone=player_anchor_contact_zone,
                    )
                )
                continue
            nearest_player = NearestPlayerContext(
                player=player,
                distance_template_units=distance,
                time_delta_ms=abs(player.timestamp_ms - anchor.timestamp_ms),
            )
            hit_candidates.append(
                _player_anchored_hit_candidate_from_context(
                    context,
                    nearest_player,
                    config,
                    net_axis_reversal=net_axis_reversal,
                    player_anchor_contact_zone=player_anchor_contact_zone,
                )
            )
            accepted = True
            break
        if not accepted:
            continue
    return evaluated_contexts, hit_candidates, rejection_diagnostics


def player_anchor_ball_candidates(
    player: PlayerProjection,
    ball_points: list[TrajectoryPoint],
    *,
    config: HitBounceCandidateConfig,
) -> list[TrajectoryPoint]:
    window_ms = max(
        config.player_time_window_ms,
        config.player_anchored_hit_lookback_ms,
        config.player_anchored_hit_lookahead_ms,
    )
    candidates = [
        point
        for point in ball_points
        if abs(point.timestamp_ms - player.timestamp_ms) <= window_ms
    ]
    if not candidates:
        return []
    contact_window_candidates = [
        point
        for point in candidates
        if _player_anchor_distance(player, point)
        <= config.player_anchored_hit_distance_max_template
    ]
    if not contact_window_candidates:
        contact_window_candidates = [
            min(
                candidates,
                key=lambda point: (
                    _player_anchor_distance(player, point),
                    abs(point.timestamp_ms - player.timestamp_ms),
                    point.frame_number,
                ),
            )
        ]
    return sorted(
        contact_window_candidates,
        key=lambda point: (
            _player_anchor_candidate_priority(player, point, config=config),
            _player_anchor_distance(player, point),
            abs(point.timestamp_ms - player.timestamp_ms),
            point.frame_number,
            point.source_ball_court_projection_observation_id or "",
        ),
    )


def _player_anchor_candidate_priority(
    player: PlayerProjection,
    point: TrajectoryPoint,
    *,
    config: HitBounceCandidateConfig,
) -> tuple[int, int, int]:
    distance = _player_anchor_distance(player, point)
    contact_zone = _player_anchor_contact_zone_payload(
        player=player,
        anchor=point,
        config=config,
        distance_template_units=distance,
    )
    return (
        0 if contact_zone.get("side_matches_player_track") is True else 1,
        0 if contact_zone.get("in_contact_zone") is True else 1,
        1 if contact_zone.get("open_court_landing_zone") is True else 0,
    )


def _player_anchor_contact_zone_payload(
    *,
    player: PlayerProjection,
    anchor: TrajectoryPoint,
    config: HitBounceCandidateConfig,
    distance_template_units: float,
) -> dict[str, Any]:
    court_side_zone = _court_side_zone_payload(anchor)
    side_matches = _court_side_matches_player_role(
        court_side_zone.get("side"),
        player.track_role_candidate,
    )
    image_distance_pixels = _image_distance_pixels(
        player_x=player.image_x,
        player_y=player.image_y,
        point_x=anchor.image_x,
        point_y=anchor.image_y,
    )
    in_contact_zone = (
        side_matches
        and distance_template_units
        <= config.player_anchored_hit_distance_max_template
    )
    strong_contact_zone = (
        side_matches
        and distance_template_units <= config.hit_player_distance_max_template
    )
    open_court_landing_zone = (
        _inside_or_near_template(anchor, config.bounce_inside_template_margin)
        and side_matches
        and not strong_contact_zone
    )
    return {
        "nearest_player_found": True,
        "track_role_candidate": player.track_role_candidate,
        "track_candidate_id": player.track_candidate_id,
        "side": court_side_zone.get("side"),
        "side_matches_player_track": side_matches,
        "distance_template_units": distance_template_units,
        "distance_threshold": config.player_anchored_hit_distance_max_template,
        "strong_distance_threshold": config.hit_player_distance_max_template,
        "time_delta_ms": abs(player.timestamp_ms - anchor.timestamp_ms),
        "in_contact_zone": in_contact_zone,
        "strong_contact_zone": strong_contact_zone,
        "open_court_landing_zone": open_court_landing_zone,
        "image_distance_pixels": (
            _round(image_distance_pixels) if image_distance_pixels is not None else None
        ),
        "image_distance_diagnostic_only": True,
        "not_hit_truth": True,
        "observation_only": True,
        "no_adjudication": True,
    }


def _image_distance_pixels(
    *,
    player_x: float | None,
    player_y: float | None,
    point_x: float | None,
    point_y: float | None,
) -> float | None:
    if player_x is None or player_y is None or point_x is None or point_y is None:
        return None
    return math.hypot(player_x - point_x, player_y - point_y)


def _closest_player_anchor_ball_point(
    player: PlayerProjection,
    ball_points: list[TrajectoryPoint],
    *,
    config: HitBounceCandidateConfig,
) -> TrajectoryPoint | None:
    candidates = player_anchor_ball_candidates(player, ball_points, config=config)
    return candidates[0] if candidates else None


def _flatten_trajectory_points(
    trajectory_segments: list[list[TrajectoryPoint]],
) -> list[TrajectoryPoint]:
    by_key: dict[tuple[int, int, str | None], TrajectoryPoint] = {}
    for segment in trajectory_segments:
        for point in segment:
            key = (
                point.timestamp_ms,
                point.frame_number,
                point.source_ball_court_projection_observation_id,
            )
            by_key[key] = point
    return sorted(by_key.values(), key=lambda point: (point.timestamp_ms, point.frame_number))


def _player_anchor_incoming_point(
    anchor: TrajectoryPoint,
    ball_points: list[TrajectoryPoint],
    *,
    config: HitBounceCandidateConfig,
) -> TrajectoryPoint | None:
    candidates = [
        point
        for point in ball_points
        if anchor.timestamp_ms - config.player_anchored_hit_lookback_ms
        <= point.timestamp_ms
        <= anchor.timestamp_ms - config.player_anchored_hit_min_pre_post_gap_ms
        and abs(anchor.court_y - point.court_y)
        >= config.player_anchored_hit_min_net_axis_delta_template
    ]
    return max(candidates, key=lambda point: (point.timestamp_ms, point.frame_number), default=None)


def _player_anchor_outgoing_point(
    anchor: TrajectoryPoint,
    ball_points: list[TrajectoryPoint],
    *,
    config: HitBounceCandidateConfig,
) -> TrajectoryPoint | None:
    candidates = [
        point
        for point in ball_points
        if anchor.timestamp_ms + config.player_anchored_hit_min_pre_post_gap_ms
        <= point.timestamp_ms
        <= anchor.timestamp_ms + config.player_anchored_hit_lookahead_ms
        and abs(point.court_y - anchor.court_y)
        >= config.player_anchored_hit_min_net_axis_delta_template
    ]
    return min(candidates, key=lambda point: (point.timestamp_ms, point.frame_number), default=None)


def _net_axis_reversal_incoming_point(
    anchor: TrajectoryPoint,
    ball_points: list[TrajectoryPoint],
    *,
    config: HitBounceCandidateConfig,
) -> TrajectoryPoint | None:
    candidates = [
        point
        for point in ball_points
        if anchor.timestamp_ms - config.net_axis_reversal_lookback_ms
        <= point.timestamp_ms
        <= anchor.timestamp_ms - config.net_axis_reversal_min_pre_post_gap_ms
        and abs(anchor.court_y - point.court_y)
        >= config.net_axis_reversal_min_delta_template
    ]
    return max(candidates, key=lambda point: (point.timestamp_ms, point.frame_number), default=None)


def _net_axis_reversal_outgoing_point(
    anchor: TrajectoryPoint,
    ball_points: list[TrajectoryPoint],
    *,
    config: HitBounceCandidateConfig,
) -> TrajectoryPoint | None:
    candidates = [
        point
        for point in ball_points
        if anchor.timestamp_ms + config.net_axis_reversal_min_pre_post_gap_ms
        <= point.timestamp_ms
        <= anchor.timestamp_ms + config.net_axis_reversal_lookahead_ms
        and abs(point.court_y - anchor.court_y)
        >= config.net_axis_reversal_min_delta_template
    ]
    return min(candidates, key=lambda point: (point.timestamp_ms, point.frame_number), default=None)


def _player_anchor_distance(player: PlayerProjection, point: TrajectoryPoint) -> float:
    return _round(math.hypot(player.court_x - point.court_x, player.court_y - point.court_y))


def _wide_window_net_axis_reversal_payload(
    *,
    incoming: TrajectoryPoint,
    anchor: TrajectoryPoint,
    outgoing: TrajectoryPoint,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    vy_before = anchor.court_y - incoming.court_y
    vy_after = outgoing.court_y - anchor.court_y
    min_delta = config.player_anchored_hit_min_net_axis_delta_template
    reversal = (
        abs(vy_before) >= min_delta
        and abs(vy_after) >= min_delta
        and vy_before * vy_after < 0
    )
    return {
        "axis": "court_y",
        "vy_before": _round(vy_before),
        "vy_after": _round(vy_after),
        "reversal": reversal,
        "min_axis_delta": min_delta,
        "incoming_frame": incoming.frame_number,
        "current_frame": anchor.frame_number,
        "outgoing_frame": outgoing.frame_number,
        "incoming_timestamp_ms": incoming.timestamp_ms,
        "current_timestamp_ms": anchor.timestamp_ms,
        "outgoing_timestamp_ms": outgoing.timestamp_ms,
        "window_method": "player_anchored_wide_window_v024",
    }


def _ball_first_net_axis_reversal_payload(
    *,
    incoming: TrajectoryPoint,
    anchor: TrajectoryPoint,
    outgoing: TrajectoryPoint,
    player_projections: list[PlayerProjection],
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    nearest_player = nearest_main_player_projection(
        anchor,
        player_projections,
        time_window_ms=max(
            config.player_time_window_ms,
            config.net_axis_reversal_lookback_ms,
        ),
    )
    vy_before = anchor.court_y - incoming.court_y
    vy_after = outgoing.court_y - anchor.court_y
    min_delta = config.net_axis_reversal_min_delta_template
    reversal = (
        abs(vy_before) >= min_delta
        and abs(vy_after) >= min_delta
        and vy_before * vy_after < 0
    )
    return {
        "axis": "court_y",
        "vy_before": _round(vy_before),
        "vy_after": _round(vy_after),
        "reversal": reversal,
        "min_axis_delta": min_delta,
        "incoming_frame": incoming.frame_number,
        "current_frame": anchor.frame_number,
        "outgoing_frame": outgoing.frame_number,
        "incoming_timestamp_ms": incoming.timestamp_ms,
        "current_timestamp_ms": anchor.timestamp_ms,
        "outgoing_timestamp_ms": outgoing.timestamp_ms,
        "lookback_ms": config.net_axis_reversal_lookback_ms,
        "lookahead_ms": config.net_axis_reversal_lookahead_ms,
        "min_pre_post_gap_ms": config.net_axis_reversal_min_pre_post_gap_ms,
        "window_method": "ball_first_net_axis_reversal_wide_window_v025",
        "player_proximity_required": False,
        "nearest_player_found": nearest_player is not None,
        "nearest_player_distance_template_units": (
            nearest_player.distance_template_units if nearest_player is not None else None
        ),
        "nearest_player_track_role_candidate": (
            nearest_player.player.track_role_candidate if nearest_player is not None else None
        ),
        "player_proximity_used_for_scoring": nearest_player is not None,
        "not_hit_truth": True,
        "observation_only": True,
        "no_adjudication": True,
    }


def trajectory_context(
    previous: TrajectoryPoint,
    current: TrajectoryPoint,
    next_point: TrajectoryPoint,
) -> TrajectoryContext | None:
    dt_before_ms = current.timestamp_ms - previous.timestamp_ms
    dt_after_ms = next_point.timestamp_ms - current.timestamp_ms
    if dt_before_ms <= 0 or dt_after_ms <= 0:
        return None
    dx_before = current.court_x - previous.court_x
    dy_before = current.court_y - previous.court_y
    dx_after = next_point.court_x - current.court_x
    dy_after = next_point.court_y - current.court_y
    speed_before = math.hypot(dx_before, dy_before) / (dt_before_ms / 1000.0)
    speed_after = math.hypot(dx_after, dy_after) / (dt_after_ms / 1000.0)
    if speed_before <= 0 and speed_after <= 0:
        return None
    direction_before = math.degrees(math.atan2(dy_before, dx_before))
    direction_after = math.degrees(math.atan2(dy_after, dx_after))
    direction_delta = angle_delta_degrees(direction_before, direction_after)
    speed_delta_fraction = abs(speed_after - speed_before) / max(
        speed_before,
        speed_after,
        1e-9,
    )
    return TrajectoryContext(
        previous=previous,
        current=current,
        next=next_point,
        direction_before_degrees=_round(direction_before),
        direction_after_degrees=_round(direction_after),
        direction_delta_degrees=_round(direction_delta),
        speed_before=_round(speed_before),
        speed_after=_round(speed_after),
        speed_delta_fraction=_round(speed_delta_fraction),
    )


def angle_delta_degrees(a: float, b: float) -> float:
    return abs((b - a + 180.0) % 360.0 - 180.0)


def nearest_main_player_projection(
    point: TrajectoryPoint,
    player_projections: list[PlayerProjection],
    *,
    time_window_ms: int,
) -> NearestPlayerContext | None:
    candidates: list[NearestPlayerContext] = []
    for player in player_projections:
        time_delta = abs(player.timestamp_ms - point.timestamp_ms)
        if time_delta > time_window_ms:
            continue
        distance = math.hypot(player.court_x - point.court_x, player.court_y - point.court_y)
        candidates.append(
            NearestPlayerContext(
                player=player,
                distance_template_units=_round(distance),
                time_delta_ms=time_delta,
            )
        )
    return min(
        candidates,
        key=lambda candidate: (
            candidate.time_delta_ms,
            candidate.distance_template_units,
            candidate.player.observation.id,
        ),
        default=None,
    )


def _net_axis_reversal_payload(
    segment: list[TrajectoryPoint],
    index: int,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    current = segment[index]
    previous = next(
        (
            point
            for point in reversed(segment[:index])
            if abs(current.court_y - point.court_y)
            >= config.hit_min_net_axis_delta_template
        ),
        None,
    )
    next_point = next(
        (
            point
            for point in segment[index + 1 :]
            if abs(point.court_y - current.court_y)
            >= config.hit_min_net_axis_delta_template
        ),
        None,
    )
    vy_before = current.court_y - previous.court_y if previous is not None else None
    vy_after = next_point.court_y - current.court_y if next_point is not None else None
    reversal = (
        vy_before is not None
        and vy_after is not None
        and abs(vy_before) >= config.hit_min_net_axis_delta_template
        and abs(vy_after) >= config.hit_min_net_axis_delta_template
        and vy_before * vy_after < 0
    )
    return {
        "axis": "court_y",
        "vy_before": _round(vy_before) if vy_before is not None else None,
        "vy_after": _round(vy_after) if vy_after is not None else None,
        "reversal": reversal,
        "min_axis_delta": config.hit_min_net_axis_delta_template,
        "previous_frame": previous.frame_number if previous is not None else None,
        "current_frame": current.frame_number,
        "next_frame": next_point.frame_number if next_point is not None else None,
        "previous_timestamp_ms": (
            previous.timestamp_ms if previous is not None else None
        ),
        "current_timestamp_ms": current.timestamp_ms,
        "next_timestamp_ms": next_point.timestamp_ms if next_point is not None else None,
    }


def _vertical_motion_proxy_payload(
    segment: list[TrajectoryPoint],
    index: int,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    current = segment[index]
    if current.image_y is None:
        return {
            "proxy_type": "image_y_descending_to_ascending_v0",
            "status": "unavailable",
            "image_y_before": None,
            "image_y_current": None,
            "image_y_after": None,
            "image_vy_before": None,
            "image_vy_after": None,
            "descending_to_ascending": False,
            "min_image_y_delta_pixels": config.bounce_min_image_y_delta_pixels,
            "proxy_warning": "image_y is camera-space proxy, not true ball height",
        }

    previous = next(
        (
            point
            for point in reversed(segment[:index])
            if point.image_y is not None
            and current.image_y - point.image_y
            >= config.bounce_min_image_y_delta_pixels
        ),
        None,
    )
    next_point = next(
        (
            point
            for point in segment[index + 1 :]
            if point.image_y is not None
            and point.image_y - current.image_y
            <= -config.bounce_min_image_y_delta_pixels
        ),
        None,
    )
    image_vy_before = (
        current.image_y - previous.image_y
        if previous is not None and previous.image_y is not None
        else None
    )
    image_vy_after = (
        next_point.image_y - current.image_y
        if next_point is not None and next_point.image_y is not None
        else None
    )
    descending_to_ascending = (
        image_vy_before is not None
        and image_vy_after is not None
        and image_vy_before >= config.bounce_min_image_y_delta_pixels
        and image_vy_after <= -config.bounce_min_image_y_delta_pixels
    )
    return {
        "proxy_type": "image_y_descending_to_ascending_v0",
        "status": "available" if previous is not None and next_point is not None else "partial",
        "image_y_before": _round(previous.image_y) if previous is not None else None,
        "image_y_current": _round(current.image_y),
        "image_y_after": _round(next_point.image_y) if next_point is not None else None,
        "image_vy_before": (
            _round(image_vy_before) if image_vy_before is not None else None
        ),
        "image_vy_after": _round(image_vy_after) if image_vy_after is not None else None,
        "descending_to_ascending": descending_to_ascending,
        "min_image_y_delta_pixels": config.bounce_min_image_y_delta_pixels,
        "previous_frame": previous.frame_number if previous is not None else None,
        "current_frame": current.frame_number,
        "next_frame": next_point.frame_number if next_point is not None else None,
        "previous_timestamp_ms": (
            previous.timestamp_ms if previous is not None else None
        ),
        "current_timestamp_ms": current.timestamp_ms,
        "next_timestamp_ms": next_point.timestamp_ms if next_point is not None else None,
        "proxy_warning": "image_y is camera-space proxy, not true ball height",
    }


def _speed_reduction_payload(
    context: TrajectoryContext,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    if context.speed_before <= 0:
        reduction_fraction = None
        speed_reduced = False
    else:
        reduction_fraction = (context.speed_before - context.speed_after) / max(
            context.speed_before,
            1e-9,
        )
        speed_reduced = reduction_fraction >= config.bounce_min_speed_reduction_fraction
    return {
        "speed_before": context.speed_before,
        "speed_after": context.speed_after,
        "speed_reduction_fraction": (
            _round(reduction_fraction) if reduction_fraction is not None else None
        ),
        "speed_reduced": speed_reduced,
        "min_speed_reduction_fraction": config.bounce_min_speed_reduction_fraction,
    }


def dedupe_event_candidates(
    candidates: list[EventCandidateDraft],
    *,
    candidate_dedupe_ms: int,
) -> list[EventCandidateDraft]:
    kept, _ = dedupe_event_candidates_with_rejections(
        candidates,
        candidate_dedupe_ms=candidate_dedupe_ms,
    )
    return kept


def dedupe_event_candidates_with_rejections(
    candidates: list[EventCandidateDraft],
    *,
    candidate_dedupe_ms: int,
) -> tuple[list[EventCandidateDraft], list[EventCandidateRejectionDiagnostic]]:
    kept: list[EventCandidateDraft] = []
    rejections: list[EventCandidateRejectionDiagnostic] = []
    for candidate in sorted(
        candidates,
        key=lambda item: (
            _candidate_preference_rank(item),
            -item.confidence,
            item.timestamp_ms,
            item.frame_number,
            item.trajectory_context.current.source_ball_court_projection_observation_id or "",
        ),
    ):
        key = _dedupe_key(candidate)
        duplicate = next(
            (
                existing
                for existing in kept
                if _dedupe_key(existing) == key
                and abs(existing.timestamp_ms - candidate.timestamp_ms)
                <= candidate_dedupe_ms
            ),
            None,
        )
        if duplicate is not None:
            if _should_preserve_pre_anchor_landing_candidate(
                candidate,
                duplicate,
                kept=kept,
                candidate_dedupe_ms=candidate_dedupe_ms,
            ):
                kept.append(candidate)
                continue
            rejection_reasons = ["deduped_lower_confidence"]
            if duplicate.candidate_method == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD:
                rejection_reasons.append("deduped_by_player_anchored_hit")
            if duplicate.candidate_method == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD:
                rejection_reasons.append("deduped_by_net_axis_reversal_hit")
            rejections.append(
                _rejection_diagnostic_from_candidate(
                    candidate,
                    rejection_reasons=rejection_reasons,
                    decision_reason="deduped_lower_confidence",
                )
            )
            continue
        kept.append(candidate)
    return (
        sorted(kept, key=lambda item: (item.timestamp_ms, item.frame_number)),
        rejections,
    )


def _candidate_preference_rank(candidate: EventCandidateDraft) -> int:
    if candidate.candidate_method == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD:
        return 0
    if candidate.candidate_method in {HIT_CANDIDATE_METHOD, HIT_FALLBACK_CANDIDATE_METHOD}:
        return 1
    if candidate.candidate_method == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD:
        return 2
    return 3


def _should_preserve_pre_anchor_landing_candidate(
    candidate: EventCandidateDraft,
    duplicate: EventCandidateDraft,
    *,
    kept: list[EventCandidateDraft],
    candidate_dedupe_ms: int,
) -> bool:
    if not (
        duplicate.candidate_method == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
        and candidate.candidate_method == HIT_FALLBACK_CANDIDATE_METHOD
        and candidate.timestamp_ms < duplicate.timestamp_ms
    ):
        return False
    return not any(
        existing is not duplicate
        and existing.candidate_method == HIT_FALLBACK_CANDIDATE_METHOD
        and _dedupe_key(existing) == _dedupe_key(candidate)
        and abs(existing.timestamp_ms - candidate.timestamp_ms) <= candidate_dedupe_ms
        and existing.timestamp_ms < duplicate.timestamp_ms
        for existing in kept
    )


def suppress_bounces_near_hits(
    hit_candidates: list[EventCandidateDraft],
    bounce_candidates: list[EventCandidateDraft],
    *,
    candidate_dedupe_ms: int,
) -> tuple[
    list[EventCandidateDraft],
    int,
    list[EventCandidateRejectionDiagnostic],
]:
    filtered_bounces: list[EventCandidateDraft] = []
    rejections: list[EventCandidateRejectionDiagnostic] = []
    suppressed_count = 0
    for bounce in bounce_candidates:
        suppressing_hit = next(
            (
                hit
                for hit in hit_candidates
                if abs(hit.timestamp_ms - bounce.timestamp_ms) <= candidate_dedupe_ms
                and hit.nearest_player is not None
                and not _is_net_axis_reversal_hit_candidate(hit)
            ),
            None,
        )
        if suppressing_hit is not None:
            suppressed_count += 1
            rejections.append(
                _rejection_diagnostic_from_candidate(
                    bounce,
                    rejection_reasons=["suppressed_by_hit_candidate"],
                    decision_reason="suppressed_by_hit_candidate",
                    suppressed_by_observation_type=suppressing_hit.observation_type,
                    suppressed_by_frame=suppressing_hit.frame_number,
                    suppressed_by_timestamp_ms=suppressing_hit.timestamp_ms,
                )
            )
            continue
        filtered_bounces.append(bounce)
    return filtered_bounces, suppressed_count, rejections


def suppress_player_anchored_hits_overlapping_bounces(
    candidates: list[EventCandidateDraft],
    *,
    config: HitBounceCandidateConfig,
) -> tuple[
    list[EventCandidateDraft],
    int,
    list[EventCandidateRejectionDiagnostic],
]:
    bounces = [
        candidate
        for candidate in candidates
        if candidate.observation_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE
    ]
    filtered: list[EventCandidateDraft] = []
    rejections: list[EventCandidateRejectionDiagnostic] = []
    suppressed_count = 0
    for candidate in candidates:
        if not _is_player_anchored_hit_candidate(candidate):
            filtered.append(candidate)
            continue
        overlapping_bounce = _overlapping_bounce_candidate(
            candidate,
            bounces,
            config=config,
        )
        if overlapping_bounce is None:
            filtered.append(
                replace(
                    candidate,
                    overlap_suppression=_overlap_suppression_payload(
                        hit=candidate,
                        bounce=None,
                        config=config,
                        suppressed=False,
                    ),
                )
            )
            continue
        overlap_payload = _overlap_suppression_payload(
            hit=candidate,
            bounce=overlapping_bounce,
            config=config,
            suppressed=True,
        )
        suppressed_count += 1
        rejections.append(
            _rejection_diagnostic_from_candidate(
                replace(candidate, overlap_suppression=overlap_payload),
                rejection_reasons=[
                    "suppressed_by_bounce_candidate_overlap",
                    "open_court_landing_zone_anchor",
                ],
                decision_reason="suppressed_by_bounce_candidate_overlap",
                suppressed_by_observation_type=overlapping_bounce.observation_type,
                suppressed_by_frame=overlapping_bounce.frame_number,
                suppressed_by_timestamp_ms=overlapping_bounce.timestamp_ms,
                overlap_suppression=overlap_payload,
            )
        )
    return (
        sorted(filtered, key=lambda item: (item.timestamp_ms, item.frame_number)),
        suppressed_count,
        rejections,
    )


def suppress_weak_net_axis_reversal_hits_overlapping_bounces(
    candidates: list[EventCandidateDraft],
    *,
    config: HitBounceCandidateConfig,
) -> tuple[
    list[EventCandidateDraft],
    int,
    list[EventCandidateRejectionDiagnostic],
]:
    bounces = [
        candidate
        for candidate in candidates
        if candidate.observation_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE
    ]
    filtered: list[EventCandidateDraft] = []
    rejections: list[EventCandidateRejectionDiagnostic] = []
    suppressed_count = 0
    for candidate in candidates:
        if not _is_weak_net_axis_reversal_hit_candidate(candidate, config=config):
            filtered.append(candidate)
            continue
        overlapping_bounce = _overlapping_bounce_candidate(
            candidate,
            bounces,
            config=config,
        )
        if overlapping_bounce is None:
            filtered.append(
                replace(
                    candidate,
                    overlap_suppression=_overlap_suppression_payload(
                        hit=candidate,
                        bounce=None,
                        config=config,
                        suppressed=False,
                    ),
                )
            )
            continue
        overlap_payload = _overlap_suppression_payload(
            hit=candidate,
            bounce=overlapping_bounce,
            config=config,
            suppressed=True,
        )
        suppressed_count += 1
        rejections.append(
            _rejection_diagnostic_from_candidate(
                replace(candidate, overlap_suppression=overlap_payload),
                rejection_reasons=["suppressed_by_bounce_candidate_overlap"],
                decision_reason="suppressed_by_bounce_candidate_overlap",
                suppressed_by_observation_type=overlapping_bounce.observation_type,
                suppressed_by_frame=overlapping_bounce.frame_number,
                suppressed_by_timestamp_ms=overlapping_bounce.timestamp_ms,
                overlap_suppression=overlap_payload,
            )
        )
    return (
        sorted(filtered, key=lambda item: (item.timestamp_ms, item.frame_number)),
        suppressed_count,
        rejections,
    )


def _is_player_anchored_hit_candidate(candidate: EventCandidateDraft) -> bool:
    return (
        candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
        and (
            candidate.candidate_method == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
            or candidate.original_candidate_method == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
        )
    )


def _is_weak_net_axis_reversal_hit_candidate(
    candidate: EventCandidateDraft,
    *,
    config: HitBounceCandidateConfig,
) -> bool:
    if candidate.observation_type != HIT_CANDIDATE_OBSERVATION_TYPE:
        return False
    if (
        candidate.candidate_method != NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
        and candidate.original_candidate_method != NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
    ):
        return False
    if candidate.nearest_player is None:
        return candidate.confidence < 0.62
    side_matches = _court_side_matches_player_role(
        _court_side_zone_payload(candidate.trajectory_context.current).get("side"),
        candidate.nearest_player.player.track_role_candidate,
    )
    return (
        candidate.nearest_player.distance_template_units
        > config.hit_player_review_distance_max_template
        or not side_matches
    ) and candidate.confidence < 0.62


def _is_net_axis_reversal_hit_candidate(candidate: EventCandidateDraft) -> bool:
    return (
        candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
        and (
            candidate.candidate_method == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
            or candidate.original_candidate_method == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
        )
    )


def _overlapping_bounce_candidate(
    hit: EventCandidateDraft,
    bounces: list[EventCandidateDraft],
    *,
    config: HitBounceCandidateConfig,
) -> EventCandidateDraft | None:
    overlaps = [
        bounce
        for bounce in bounces
        if abs(hit.timestamp_ms - bounce.timestamp_ms) <= config.candidate_dedupe_ms
        and _candidate_court_distance(hit, bounce)
        <= config.event_overlap_distance_template
    ]
    return min(
        overlaps,
        key=lambda bounce: (
            _candidate_court_distance(hit, bounce),
            abs(hit.timestamp_ms - bounce.timestamp_ms),
            bounce.frame_number,
        ),
        default=None,
    )


def _candidate_court_distance(
    a: EventCandidateDraft,
    b: EventCandidateDraft,
) -> float:
    a_point = a.trajectory_context.current
    b_point = b.trajectory_context.current
    return _round(math.hypot(a_point.court_x - b_point.court_x, a_point.court_y - b_point.court_y))


def _overlap_suppression_payload(
    *,
    hit: EventCandidateDraft,
    bounce: EventCandidateDraft | None,
    config: HitBounceCandidateConfig,
    suppressed: bool,
) -> dict[str, Any]:
    if bounce is None:
        return {
            "overlaps_bounce_candidate": False,
            "overlap_distance_template": None,
            "overlap_time_delta_ms": None,
            "threshold": config.event_overlap_distance_template,
            "suppressed": False,
            "reason": None,
        }
    return {
        "overlaps_bounce_candidate": True,
        "overlap_distance_template": _candidate_court_distance(hit, bounce),
        "overlap_time_delta_ms": abs(hit.timestamp_ms - bounce.timestamp_ms),
        "threshold": config.event_overlap_distance_template,
        "suppressed": suppressed,
        "reason": (
            "bounce_candidate_overlap_without_strong_contact_zone"
            if suppressed
            else None
        ),
        "source_bounce_frame": bounce.frame_number,
        "source_bounce_timestamp_ms": bounce.timestamp_ms,
        "source_bounce_candidate_method": bounce.candidate_method,
        "candidate_only": True,
        "not_hit_truth": True,
        "not_bounce_truth": True,
        "not_in_out_truth": True,
        "observation_only": True,
        "no_adjudication": True,
    }


def apply_side_zone_sequence_classification(
    candidates: list[EventCandidateDraft],
    *,
    config: HitBounceCandidateConfig,
) -> tuple[list[EventCandidateDraft], dict[str, int]]:
    ordered = sorted(candidates, key=lambda item: (item.timestamp_ms, item.frame_number))
    final_candidates: list[EventCandidateDraft] = []
    previous_final_type: str | None = None
    reclassified_hit_to_bounce_count = 0
    reclassified_bounce_to_hit_count = 0
    sequence_prior_applied_count = 0
    for sequence_index, candidate in enumerate(ordered):
        original_type = candidate.original_observation_type or candidate.observation_type
        expected_type = _expected_next_candidate_type(previous_final_type)
        court_side_zone = _court_side_zone_payload(candidate.trajectory_context.current)
        player_contact_zone = _player_contact_zone_payload(
            candidate,
            config=config,
            court_side_zone=court_side_zone,
        )
        court_landing_zone = _court_landing_zone_payload(
            candidate,
            config=config,
            court_side_zone=court_side_zone,
            player_contact_zone=player_contact_zone,
        )
        final_type = candidate.observation_type
        final_method = candidate.candidate_method
        reclassification_reason: str | None = None
        sequence_prior_applied = False
        if (
            candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
            and expected_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE
            and _hit_candidate_can_be_landing_zone_bounce(
                candidate,
                court_landing_zone=court_landing_zone,
            )
        ):
            final_type = BOUNCE_CANDIDATE_OBSERVATION_TYPE
            final_method = SIDE_ZONE_SEQUENCE_BOUNCE_METHOD
            reclassification_reason = "court_landing_zone_over_player_contact_zone"
            sequence_prior_applied = True
            reclassified_hit_to_bounce_count += 1
        elif (
            candidate.observation_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE
            and player_contact_zone.get("in_contact_zone") is True
            and (
                expected_type == HIT_CANDIDATE_OBSERVATION_TYPE
                or player_contact_zone.get("side_matches_player_track") is True
            )
        ):
            final_type = HIT_CANDIDATE_OBSERVATION_TYPE
            final_method = SIDE_ZONE_SEQUENCE_HIT_METHOD
            reclassification_reason = "player_contact_zone_over_court_landing_zone"
            sequence_prior_applied = expected_type == HIT_CANDIDATE_OBSERVATION_TYPE
            reclassified_bounce_to_hit_count += 1
        if sequence_prior_applied:
            sequence_prior_applied_count += 1
        candidate_sequence = {
            "sequence_index": sequence_index,
            "previous_candidate_type": previous_final_type,
            "expected_candidate_type": expected_type,
            "sequence_prior_applied": sequence_prior_applied,
            "sequence_pattern": "hit_bounce_alternation_v0",
        }
        candidate_reclassification = {
            "original_candidate_type": original_type,
            "final_candidate_type": final_type,
            "reason": reclassification_reason,
            "reclassified": reclassification_reason is not None,
        }
        reason_codes = _final_reason_codes(
            candidate,
            final_type=final_type,
            reclassification_reason=reclassification_reason,
            sequence_prior_applied=sequence_prior_applied,
            player_contact_zone=player_contact_zone,
        )
        final_candidate = replace(
            candidate,
            observation_type=final_type,  # type: ignore[arg-type]
            candidate_method=final_method,
            reason_codes=reason_codes,
            original_observation_type=original_type,  # type: ignore[arg-type]
            original_candidate_method=(
                candidate.original_candidate_method or candidate.candidate_method
            ),
            court_side_zone=court_side_zone,
            player_contact_zone=player_contact_zone,
            court_landing_zone=court_landing_zone,
            candidate_reclassification=candidate_reclassification,
            candidate_sequence=candidate_sequence,
            candidate_decision={
                "selected_candidate_type": final_type,
                "original_candidate_type": original_type,
                "suppressed_candidate_types": (
                    [BOUNCE_CANDIDATE_OBSERVATION_TYPE]
                    if final_type == HIT_CANDIDATE_OBSERVATION_TYPE
                    else []
                ),
                "reason": reclassification_reason
                or candidate.candidate_decision.get("reason"),
                "classification_priority": "side_zone_sequence_candidate_prior",
            },
        )
        final_candidates.append(final_candidate)
        previous_final_type = final_type
    return final_candidates, {
        "reclassified_hit_to_bounce_count": reclassified_hit_to_bounce_count,
        "reclassified_bounce_to_hit_count": reclassified_bounce_to_hit_count,
        "sequence_prior_applied_count": sequence_prior_applied_count,
    }


def _expected_next_candidate_type(previous_final_type: str | None) -> str | None:
    if previous_final_type == HIT_CANDIDATE_OBSERVATION_TYPE:
        return BOUNCE_CANDIDATE_OBSERVATION_TYPE
    if previous_final_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE:
        return HIT_CANDIDATE_OBSERVATION_TYPE
    return None


def _court_side_zone_payload(point: TrajectoryPoint) -> dict[str, Any]:
    if abs(point.court_y - COURT_SIDE_SPLIT_Y) <= COURT_MIDCOURT_MARGIN_Y:
        side = "midcourt_net_zone"
    elif point.court_y < COURT_SIDE_SPLIT_Y:
        side = "near_side"
    else:
        side = "far_side"
    return {
        "side": side,
        "court_y": _round(point.court_y),
        "side_split_y": COURT_SIDE_SPLIT_Y,
        "midcourt_margin_y": COURT_MIDCOURT_MARGIN_Y,
        "court_y_convention": COURT_Y_CONVENTION,
    }


def _player_contact_zone_payload(
    candidate: EventCandidateDraft,
    *,
    config: HitBounceCandidateConfig,
    court_side_zone: dict[str, Any],
) -> dict[str, Any]:
    nearest_player = candidate.nearest_player
    if nearest_player is None:
        return {
            "nearest_player_found": False,
            "track_role_candidate": None,
            "distance_template_units": None,
            "time_delta_ms": None,
            "in_contact_zone": False,
            "strong_contact_zone": False,
            "threshold": config.hit_player_review_distance_max_template,
            "strong_threshold": config.hit_player_distance_max_template,
            "side_matches_player_track": False,
        }
    side_matches = _court_side_matches_player_role(
        court_side_zone.get("side"),
        nearest_player.player.track_role_candidate,
    )
    in_contact_zone = (
        nearest_player.distance_template_units
        <= config.hit_player_review_distance_max_template
        and side_matches
    )
    strong_contact_zone = (
        nearest_player.distance_template_units <= config.hit_player_distance_max_template
        and candidate.net_axis_reversal is not None
        and candidate.net_axis_reversal.get("reversal") is True
        and side_matches
    )
    return {
        "nearest_player_found": True,
        "track_role_candidate": nearest_player.player.track_role_candidate,
        "track_candidate_id": nearest_player.player.track_candidate_id,
        "distance_template_units": nearest_player.distance_template_units,
        "time_delta_ms": nearest_player.time_delta_ms,
        "in_contact_zone": in_contact_zone,
        "strong_contact_zone": strong_contact_zone,
        "threshold": config.hit_player_review_distance_max_template,
        "strong_threshold": config.hit_player_distance_max_template,
        "side_matches_player_track": side_matches,
    }


def _court_landing_zone_payload(
    candidate: EventCandidateDraft,
    *,
    config: HitBounceCandidateConfig,
    court_side_zone: dict[str, Any],
    player_contact_zone: dict[str, Any],
) -> dict[str, Any]:
    inside_or_near = _inside_or_near_template(
        candidate.trajectory_context.current,
        config.bounce_inside_template_margin,
    )
    away_from_player = (
        candidate.nearest_player is None
        or candidate.nearest_player.distance_template_units
        >= config.bounce_player_distance_min_template
    )
    landing_zone_candidate = inside_or_near and (
        away_from_player or player_contact_zone.get("strong_contact_zone") is not True
    )
    return {
        "inside_or_near_court": inside_or_near,
        "away_from_player": away_from_player,
        "side": court_side_zone.get("side"),
        "landing_zone_candidate": landing_zone_candidate,
        "margin": config.bounce_inside_template_margin,
    }


def _court_side_matches_player_role(side: Any, role: str | None) -> bool:
    if role == "near_player_track_candidate":
        return side == "near_side"
    if role == "far_player_track_candidate":
        return side == "far_side"
    return False


def _hit_candidate_can_be_landing_zone_bounce(
    candidate: EventCandidateDraft,
    *,
    court_landing_zone: dict[str, Any],
) -> bool:
    if court_landing_zone.get("landing_zone_candidate") is not True:
        return False
    if candidate.candidate_method == HIT_FALLBACK_CANDIDATE_METHOD:
        return True
    return (
        candidate.net_axis_reversal is None
        or candidate.net_axis_reversal.get("reversal") is not True
    )


def _final_reason_codes(
    candidate: EventCandidateDraft,
    *,
    final_type: str,
    reclassification_reason: str | None,
    sequence_prior_applied: bool,
    player_contact_zone: dict[str, Any],
) -> list[str]:
    reason_codes = list(dict.fromkeys(candidate.reason_codes))
    if final_type == HIT_CANDIDATE_OBSERVATION_TYPE:
        if player_contact_zone.get("in_contact_zone") is True:
            reason_codes.append("player_contact_zone")
        if player_contact_zone.get("side_matches_player_track") is True:
            reason_codes.append("side_matches_player_track")
        if candidate.candidate_method == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD:
            reason_codes.append("player_proximity_not_required")
        if sequence_prior_applied:
            reason_codes.append("sequence_hit_prior")
    else:
        reason_codes.append("court_landing_zone")
        if sequence_prior_applied:
            reason_codes.append("sequence_bounce_prior")
    if reclassification_reason is not None:
        if reclassification_reason == "court_landing_zone_over_player_contact_zone":
            reason_codes.append("reclassified_from_hit_candidate")
        elif reclassification_reason == "player_contact_zone_over_court_landing_zone":
            reason_codes.append("reclassified_from_bounce_candidate")
    return list(dict.fromkeys(reason_codes))


def _hit_signal_for_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
) -> Literal["net_axis_reversal", "player_proximate_speed_change_fallback"] | None:
    if nearest_player is None:
        return None
    if nearest_player.distance_template_units > config.hit_player_review_distance_max_template:
        return None
    strong_direction_change = (
        context.direction_delta_degrees >= config.hit_min_direction_delta_degrees
    )
    meaningful_speed_change = (
        context.speed_delta_fraction >= config.hit_min_speed_delta_fraction
    )
    relaxed_contact_change = (
        context.direction_delta_degrees
        >= config.hit_near_player_direction_delta_degrees
        or meaningful_speed_change
    )
    close_contact_zone = (
        nearest_player.distance_template_units <= config.hit_player_distance_max_template
    )
    if net_axis_reversal.get("reversal") is True and (
        strong_direction_change or (close_contact_zone and relaxed_contact_change)
    ):
        return "net_axis_reversal"
    fallback_speed_change = (
        context.speed_delta_fraction
        >= config.hit_contact_fallback_min_speed_delta_fraction
    )
    fallback_direction_change = (
        context.direction_delta_degrees
        >= config.hit_contact_fallback_min_direction_delta_degrees
    )
    if close_contact_zone and fallback_speed_change and fallback_direction_change:
        return "player_proximate_speed_change_fallback"
    return None


def _bounce_signal_for_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    vertical_motion_proxy: dict[str, Any],
    speed_reduction: dict[str, Any],
) -> Literal["vertical_proxy", "speed_reduction_fallback"] | None:
    away_from_player = (
        nearest_player is None
        or nearest_player.distance_template_units
        >= config.bounce_player_distance_min_template
    )
    inside_or_near_court = _inside_or_near_template(
        context.current,
        config.bounce_inside_template_margin,
    )
    preferred = (
        away_from_player
        and vertical_motion_proxy.get("descending_to_ascending") is True
        and speed_reduction.get("speed_reduced") is True
        and inside_or_near_court
    )
    if preferred:
        return "vertical_proxy"
    speed_reduction_fraction = float(
        speed_reduction.get("speed_reduction_fraction") or 0.0
    )
    fallback = (
        config.bounce_fallback_enabled
        and away_from_player
        and inside_or_near_court
        and speed_reduction_fraction
        >= config.bounce_fallback_min_speed_reduction_fraction
        and context.direction_delta_degrees >= config.bounce_min_direction_delta_degrees
    )
    if fallback:
        return "speed_reduction_fallback"
    return None


def _hit_candidate_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
    hit_signal: Literal["net_axis_reversal", "player_proximate_speed_change_fallback"],
) -> EventCandidateDraft:
    proximity_score = 1.0 - min(
        nearest_player.distance_template_units
        / max(config.hit_player_review_distance_max_template, 1e-9),
        1.0,
    )
    axis_strength = (
        (abs(float(net_axis_reversal.get("vy_before") or 0.0)))
        + (abs(float(net_axis_reversal.get("vy_after") or 0.0)))
    ) / max(config.hit_min_net_axis_delta_template * 4.0, 1e-9)
    axis_score = min(axis_strength, 1.0)
    if hit_signal == "player_proximate_speed_change_fallback":
        axis_score *= 0.35
    direction_score = min(context.direction_delta_degrees / 90.0, 1.0)
    speed_score = min(context.speed_delta_fraction, 1.0)
    time_score = 1.0 - min(
        nearest_player.time_delta_ms / max(config.player_time_window_ms, 1),
        1.0,
    )
    confidence = min(
        HIT_CONFIDENCE_CAP,
        0.15
        + 0.27 * proximity_score
        + 0.22 * axis_score
        + 0.16 * direction_score
        + 0.08 * speed_score
        + 0.05 * time_score,
    )
    reason_codes = [
        "near_main_player_projection",
        "trajectory_direction_change",
        "player_proximate_event_priority",
    ]
    candidate_method = HIT_CANDIDATE_METHOD
    decision_reason = "player_proximate_net_axis_reversal"
    if hit_signal == "net_axis_reversal":
        reason_codes.append("net_axis_reversal")
    else:
        candidate_method = HIT_FALLBACK_CANDIDATE_METHOD
        decision_reason = "player_proximate_speed_change_fallback"
        reason_codes.extend(
            [
                "player_proximate_speed_change_fallback",
                "net_axis_reversal_not_required_for_fallback",
            ]
        )
    if context.speed_delta_fraction >= config.hit_min_speed_delta_fraction:
        reason_codes.append("speed_change_candidate")
    if nearest_player.time_delta_ms <= config.player_time_window_ms:
        reason_codes.append("within_time_window")
    return EventCandidateDraft(
        observation_type=HIT_CANDIDATE_OBSERVATION_TYPE,
        candidate_method=candidate_method,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=reason_codes,
        confidence=_round(confidence),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.hit_player_review_distance_max_template,
            away_from_player=False,
        ),
        candidate_decision={
            "selected_candidate_type": HIT_CANDIDATE_OBSERVATION_TYPE,
            "suppressed_candidate_types": [BOUNCE_CANDIDATE_OBSERVATION_TYPE],
            "reason": decision_reason,
            "classification_priority": "player_anchored_hit_recall_then_sequence_prior",
        },
        net_axis_reversal=net_axis_reversal,
    )


def _net_axis_reversal_hit_candidate_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
) -> EventCandidateDraft:
    axis_strength = (
        abs(float(net_axis_reversal.get("vy_before") or 0.0))
        + abs(float(net_axis_reversal.get("vy_after") or 0.0))
    ) / max(config.net_axis_reversal_min_delta_template * 4.0, 1e-9)
    axis_score = min(axis_strength, 1.0)
    direction_score = min(context.direction_delta_degrees / 90.0, 1.0)
    inside_score = (
        1.0
        if _inside_or_near_template(context.current, config.bounce_inside_template_margin)
        else 0.0
    )
    proximity_score = 0.0
    time_score = 0.0
    side_score = 0.0
    if nearest_player is not None:
        proximity_score = 1.0 - min(
            nearest_player.distance_template_units
            / max(config.hit_player_review_distance_max_template, 1e-9),
            1.0,
        )
        time_score = 1.0 - min(
            nearest_player.time_delta_ms / max(config.player_time_window_ms, 1),
            1.0,
        )
        side_score = (
            1.0
            if _court_side_matches_player_role(
                _court_side_zone_payload(context.current).get("side"),
                nearest_player.player.track_role_candidate,
            )
            else 0.0
        )
    confidence = min(
        HIT_CONFIDENCE_CAP,
        0.20
        + 0.28 * axis_score
        + 0.16 * direction_score
        + 0.10 * inside_score
        + 0.08 * proximity_score
        + 0.04 * side_score
        + 0.04 * time_score,
    )
    reason_codes = [
        "net_axis_reversal",
        "ball_first_reversal_recall",
        "player_proximity_not_required",
    ]
    if nearest_player is not None:
        reason_codes.extend(
            [
                "nearest_main_player_projection",
                "player_proximity_diagnostic",
            ]
        )
        if side_score > 0:
            reason_codes.append("side_matches_player_track")
    return EventCandidateDraft(
        observation_type=HIT_CANDIDATE_OBSERVATION_TYPE,
        candidate_method=NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=reason_codes,
        confidence=_round(confidence),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.hit_player_review_distance_max_template,
            away_from_player=False,
        ),
        candidate_decision={
            "selected_candidate_type": HIT_CANDIDATE_OBSERVATION_TYPE,
            "suppressed_candidate_types": [BOUNCE_CANDIDATE_OBSERVATION_TYPE],
            "reason": "ball_first_net_axis_reversal",
            "classification_priority": "net_axis_reversal_hit_recall_then_sequence_prior",
            "player_proximity_required": False,
        },
        net_axis_reversal=net_axis_reversal,
        net_axis_reversal_recall=_net_axis_reversal_recall_payload(
            context=context,
            nearest_player=nearest_player,
            config=config,
            net_axis_reversal=net_axis_reversal,
        ),
    )


def _player_anchored_hit_candidate_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
    player_anchor_contact_zone: dict[str, Any],
) -> EventCandidateDraft:
    recall_payload = _player_anchored_hit_recall_payload(
        context=context,
        nearest_player=nearest_player,
        config=config,
        net_axis_reversal=net_axis_reversal,
        player_anchor_contact_zone=player_anchor_contact_zone,
    )
    proximity_score = 1.0 - min(
        nearest_player.distance_template_units
        / max(config.player_anchored_hit_distance_max_template, 1e-9),
        1.0,
    )
    axis_strength = (
        abs(float(net_axis_reversal.get("vy_before") or 0.0))
        + abs(float(net_axis_reversal.get("vy_after") or 0.0))
    ) / max(config.player_anchored_hit_min_net_axis_delta_template * 4.0, 1e-9)
    axis_score = min(axis_strength, 1.0)
    side_score = (
        1.0
        if _court_side_matches_player_role(
            _court_side_zone_payload(context.current).get("side"),
            nearest_player.player.track_role_candidate,
        )
        else 0.0
    )
    timing_score = 1.0 - min(
        nearest_player.time_delta_ms
        / max(config.player_anchored_hit_lookback_ms, 1),
        1.0,
    )
    direction_score = min(context.direction_delta_degrees / 90.0, 1.0)
    confidence = min(
        HIT_CONFIDENCE_CAP,
        0.14
        + 0.24 * proximity_score
        + 0.24 * axis_score
        + 0.13 * direction_score
        + 0.10 * timing_score
        + 0.05 * side_score,
    )
    return EventCandidateDraft(
        observation_type=HIT_CANDIDATE_OBSERVATION_TYPE,
        candidate_method=PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=[
            "player_anchored_hit_recall",
            "near_main_player_projection",
            "net_axis_reversal",
            "wide_window_net_axis_reversal",
            "side_matches_player_track",
            "within_player_anchor_window",
        ],
        confidence=_round(confidence),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.player_anchored_hit_distance_max_template,
            away_from_player=False,
        ),
        candidate_decision={
            "selected_candidate_type": HIT_CANDIDATE_OBSERVATION_TYPE,
            "suppressed_candidate_types": [BOUNCE_CANDIDATE_OBSERVATION_TYPE],
            "reason": "player_anchored_net_axis_reversal",
            "classification_priority": "player_anchored_hit_recall_then_sequence_prior",
        },
        net_axis_reversal=net_axis_reversal,
        player_anchored_hit_recall=recall_payload,
        player_anchor_contact_zone=player_anchor_contact_zone,
    )


def _net_axis_reversal_recall_payload(
    *,
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    net_axis_reversal: dict[str, Any],
) -> dict[str, Any]:
    return {
        "enabled": config.net_axis_reversal_hit_enabled,
        "candidate_method": NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD,
        "player_proximity_required": False,
        "incoming_frame": context.previous.frame_number,
        "incoming_timestamp_ms": context.previous.timestamp_ms,
        "anchor_frame": context.current.frame_number,
        "anchor_timestamp_ms": context.current.timestamp_ms,
        "outgoing_frame": context.next.frame_number,
        "outgoing_timestamp_ms": context.next.timestamp_ms,
        "lookback_ms": config.net_axis_reversal_lookback_ms,
        "lookahead_ms": config.net_axis_reversal_lookahead_ms,
        "min_pre_post_gap_ms": config.net_axis_reversal_min_pre_post_gap_ms,
        "vy_before": net_axis_reversal.get("vy_before"),
        "vy_after": net_axis_reversal.get("vy_after"),
        "net_axis_reversal": net_axis_reversal.get("reversal") is True,
        "nearest_player_found": nearest_player is not None,
        "nearest_player_distance_template_units": (
            nearest_player.distance_template_units if nearest_player is not None else None
        ),
        "nearest_player_track_role_candidate": (
            nearest_player.player.track_role_candidate if nearest_player is not None else None
        ),
        "player_proximity_used_for_scoring": nearest_player is not None,
        "not_hit_truth": True,
        "observation_only": True,
        "no_adjudication": True,
    }


def _player_anchored_hit_recall_payload(
    *,
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext,
    config: HitBounceCandidateConfig,
    net_axis_reversal: dict[str, Any],
    player_anchor_contact_zone: dict[str, Any],
) -> dict[str, Any]:
    player = nearest_player.player
    return {
        "enabled": config.player_anchored_hit_enabled,
        "candidate_method": PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
        "anchor_player_observation_id": player.observation.id,
        "anchor_track_role_candidate": player.track_role_candidate,
        "anchor_track_candidate_id": player.track_candidate_id,
        "anchor_frame": player.frame_number,
        "anchor_timestamp_ms": player.timestamp_ms,
        "anchor_ball_frame": context.current.frame_number,
        "anchor_ball_timestamp_ms": context.current.timestamp_ms,
        "incoming_frame": context.previous.frame_number,
        "incoming_timestamp_ms": context.previous.timestamp_ms,
        "outgoing_frame": context.next.frame_number,
        "outgoing_timestamp_ms": context.next.timestamp_ms,
        "lookback_ms": config.player_anchored_hit_lookback_ms,
        "lookahead_ms": config.player_anchored_hit_lookahead_ms,
        "min_pre_post_gap_ms": config.player_anchored_hit_min_pre_post_gap_ms,
        "distance_template_units": nearest_player.distance_template_units,
        "distance_threshold": config.player_anchored_hit_distance_max_template,
        "contact_zone": player_anchor_contact_zone,
        "vy_before": net_axis_reversal.get("vy_before"),
        "vy_after": net_axis_reversal.get("vy_after"),
        "net_axis_reversal": net_axis_reversal.get("reversal") is True,
        "not_hit_truth": True,
        "observation_only": True,
        "no_adjudication": True,
    }


def _bounce_candidate_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    vertical_motion_proxy: dict[str, Any],
    speed_reduction: dict[str, Any],
    bounce_signal: Literal["vertical_proxy", "speed_reduction_fallback"],
) -> EventCandidateDraft:
    image_vy_before = abs(float(vertical_motion_proxy.get("image_vy_before") or 0.0))
    image_vy_after = abs(float(vertical_motion_proxy.get("image_vy_after") or 0.0))
    vertical_score = min(
        (image_vy_before + image_vy_after)
        / max(config.bounce_min_image_y_delta_pixels * 12.0, 1e-9),
        1.0,
    )
    speed_reduction_fraction = float(
        speed_reduction.get("speed_reduction_fraction") or 0.0
    )
    speed_score = min(
        speed_reduction_fraction
        / max(config.bounce_min_speed_reduction_fraction * 4.0, 1e-9),
        1.0,
    )
    away_score = (
        1.0
        if nearest_player is None
        else min(
            nearest_player.distance_template_units
            / max(config.bounce_player_distance_min_template * 2.0, 1e-9),
            1.0,
        )
    )
    inside_score = (
        1.0
        if context.current.inside_template_bounds
        else 0.6
        if _inside_or_near_template(context.current, config.bounce_inside_template_margin)
        else 0.0
    )
    confidence = min(
        BOUNCE_CONFIDENCE_CAP,
        0.12
        + 0.28 * vertical_score
        + 0.18 * speed_score
        + 0.20 * away_score
        + 0.15 * inside_score
    )
    if bounce_signal == "speed_reduction_fallback":
        confidence = min(confidence, 0.42)
    reason_codes = [
        "speed_reduction_candidate",
        "away_from_main_player_projection",
        "inside_or_near_court_template",
    ]
    candidate_method = BOUNCE_CANDIDATE_METHOD
    decision_reason = "away_from_player_descending_ascending_speed_reduction"
    if bounce_signal == "vertical_proxy":
        reason_codes.append("descending_to_ascending_image_proxy")
    else:
        candidate_method = BOUNCE_FALLBACK_CANDIDATE_METHOD
        decision_reason = "away_from_player_speed_reduction_fallback"
        reason_codes.append("vertical_proxy_partial_or_unavailable")
    if context.direction_delta_degrees >= config.bounce_min_direction_delta_degrees:
        reason_codes.append("trajectory_direction_change")
    if context.speed_delta_fraction >= 0.2:
        reason_codes.append("local_motion_discontinuity")
    return EventCandidateDraft(
        observation_type=BOUNCE_CANDIDATE_OBSERVATION_TYPE,
        candidate_method=candidate_method,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=reason_codes,
        confidence=_round(confidence),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.bounce_player_distance_min_template,
            away_from_player=(
                nearest_player is None
                or nearest_player.distance_template_units
                >= config.bounce_player_distance_min_template
            ),
        ),
        candidate_decision={
            "selected_candidate_type": BOUNCE_CANDIDATE_OBSERVATION_TYPE,
            "suppressed_candidate_types": [],
            "reason": decision_reason,
            "classification_priority": "player_anchored_hit_recall_then_sequence_prior",
        },
        vertical_motion_proxy=vertical_motion_proxy,
        speed_reduction=speed_reduction,
    )


def _rejection_reasons_for_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
    vertical_motion_proxy: dict[str, Any],
    speed_reduction: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if context.previous is None:
        reasons.append("missing_previous_point")
    if context.next is None:
        reasons.append("missing_next_point")
    if context.current.image_y is None:
        reasons.append("missing_source_image_point")
    if nearest_player is None:
        reasons.append("no_nearest_player_in_time_window")
    elif nearest_player.distance_template_units > config.hit_player_distance_max_template:
        reasons.append("player_too_far_for_hit")
    if net_axis_reversal.get("reversal") is not True:
        reasons.append("no_net_axis_reversal")
        if (
            net_axis_reversal.get("vy_before") is None
            or net_axis_reversal.get("vy_after") is None
        ):
            reasons.append("net_axis_delta_below_threshold")
    if vertical_motion_proxy.get("descending_to_ascending") is not True:
        reasons.append("no_descending_to_ascending_proxy")
    if speed_reduction.get("speed_reduced") is not True:
        reasons.append("no_speed_reduction")
    if not _inside_or_near_template(context.current, config.bounce_inside_template_margin):
        reasons.append("not_inside_or_near_court")
    if (
        nearest_player is not None
        and nearest_player.distance_template_units
        < config.bounce_player_distance_min_template
    ):
        reasons.append("near_player_so_not_bounce")
    return sorted(set(reasons))


def _rejection_diagnostic_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
    vertical_motion_proxy: dict[str, Any],
    speed_reduction: dict[str, Any],
    rejection_reasons: list[str],
) -> EventCandidateRejectionDiagnostic:
    return EventCandidateRejectionDiagnostic(
        trajectory_context=context,
        nearest_player=nearest_player,
        net_axis_reversal=net_axis_reversal,
        vertical_motion_proxy=vertical_motion_proxy,
        speed_reduction=speed_reduction,
        inside_or_near_court_template=_inside_or_near_template(
            context.current,
            config.bounce_inside_template_margin,
        ),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.hit_player_distance_max_template,
            away_from_player=(
                nearest_player is None
                or nearest_player.distance_template_units
                >= config.bounce_player_distance_min_template
            ),
        ),
        candidate_decision={
            "selected_candidate_type": None,
            "reason": "rejected",
            "rejection_reasons": rejection_reasons,
            "classification_priority": "player_anchored_hit_recall_then_sequence_prior",
        },
        rejection_reasons=rejection_reasons,
    )


def _player_anchor_rejection_diagnostic(
    *,
    player: PlayerProjection,
    anchor: TrajectoryPoint | None,
    incoming: TrajectoryPoint | None,
    outgoing: TrajectoryPoint | None,
    config: HitBounceCandidateConfig,
    rejection_reasons: list[str],
    distance_template_units: float | None = None,
    net_axis_reversal: dict[str, Any] | None = None,
    player_anchor_contact_zone: dict[str, Any] | None = None,
) -> EventCandidateRejectionDiagnostic:
    current = anchor or _synthetic_player_anchor_point(player)
    previous = incoming or _synthetic_neighbor_point(
        current,
        timestamp_ms=current.timestamp_ms - 1,
        frame_number=current.frame_number - 1,
    )
    next_point = outgoing or _synthetic_neighbor_point(
        current,
        timestamp_ms=current.timestamp_ms + 1,
        frame_number=current.frame_number + 1,
    )
    context = trajectory_context(previous, current, next_point) or TrajectoryContext(
        previous=previous,
        current=current,
        next=next_point,
        direction_before_degrees=0.0,
        direction_after_degrees=0.0,
        direction_delta_degrees=0.0,
        speed_before=0.0,
        speed_after=0.0,
        speed_delta_fraction=0.0,
    )
    nearest_player = (
        NearestPlayerContext(
            player=player,
            distance_template_units=distance_template_units,
            time_delta_ms=abs(player.timestamp_ms - current.timestamp_ms),
        )
        if distance_template_units is not None
        else None
    )
    recall_payload = {
        "enabled": config.player_anchored_hit_enabled,
        "candidate_method": PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
        "anchor_player_observation_id": player.observation.id,
        "anchor_track_role_candidate": player.track_role_candidate,
        "anchor_track_candidate_id": player.track_candidate_id,
        "anchor_frame": player.frame_number,
        "anchor_timestamp_ms": player.timestamp_ms,
        "anchor_ball_frame": anchor.frame_number if anchor is not None else None,
        "anchor_ball_timestamp_ms": anchor.timestamp_ms if anchor is not None else None,
        "incoming_frame": incoming.frame_number if incoming is not None else None,
        "incoming_timestamp_ms": incoming.timestamp_ms if incoming is not None else None,
        "outgoing_frame": outgoing.frame_number if outgoing is not None else None,
        "outgoing_timestamp_ms": outgoing.timestamp_ms if outgoing is not None else None,
        "lookback_ms": config.player_anchored_hit_lookback_ms,
        "lookahead_ms": config.player_anchored_hit_lookahead_ms,
        "min_pre_post_gap_ms": config.player_anchored_hit_min_pre_post_gap_ms,
        "distance_template_units": distance_template_units,
        "distance_threshold": config.player_anchored_hit_distance_max_template,
        "contact_zone": player_anchor_contact_zone,
        "net_axis_reversal": (
            net_axis_reversal.get("reversal") is True
            if net_axis_reversal is not None
            else False
        ),
        "diagnostic_only": True,
        "not_hit_truth": True,
        "observation_only": True,
        "no_adjudication": True,
    }
    return EventCandidateRejectionDiagnostic(
        trajectory_context=context,
        nearest_player=nearest_player,
        net_axis_reversal=net_axis_reversal or {},
        vertical_motion_proxy={},
        speed_reduction={},
        inside_or_near_court_template=_inside_or_near_template(
            current,
            config.bounce_inside_template_margin,
        ),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.player_anchored_hit_distance_max_template,
            away_from_player=False,
        ),
        candidate_decision={
            "selected_candidate_type": None,
            "reason": "player_anchored_hit_recall_rejected",
            "rejection_reasons": rejection_reasons,
            "classification_priority": "player_anchored_hit_recall_then_sequence_prior",
            "diagnostic_source": "player_anchored_hit_recall",
        },
        rejection_reasons=rejection_reasons,
        diagnostic_source="player_anchored_hit_recall",
        player_anchored_hit_recall=recall_payload,
        player_anchor_contact_zone=player_anchor_contact_zone,
    )


def _net_axis_reversal_rejection_diagnostic(
    *,
    anchor: TrajectoryPoint,
    incoming: TrajectoryPoint | None,
    outgoing: TrajectoryPoint | None,
    player_projections: list[PlayerProjection],
    config: HitBounceCandidateConfig,
    rejection_reasons: list[str],
    net_axis_reversal: dict[str, Any] | None = None,
) -> EventCandidateRejectionDiagnostic:
    previous = incoming or _synthetic_neighbor_point(
        anchor,
        timestamp_ms=anchor.timestamp_ms - 1,
        frame_number=anchor.frame_number - 1,
    )
    next_point = outgoing or _synthetic_neighbor_point(
        anchor,
        timestamp_ms=anchor.timestamp_ms + 1,
        frame_number=anchor.frame_number + 1,
    )
    context = trajectory_context(previous, anchor, next_point) or TrajectoryContext(
        previous=previous,
        current=anchor,
        next=next_point,
        direction_before_degrees=0.0,
        direction_after_degrees=0.0,
        direction_delta_degrees=0.0,
        speed_before=0.0,
        speed_after=0.0,
        speed_delta_fraction=0.0,
    )
    nearest_player = nearest_main_player_projection(
        anchor,
        player_projections,
        time_window_ms=max(
            config.player_time_window_ms,
            config.net_axis_reversal_lookback_ms,
        ),
    )
    recall_payload = _net_axis_reversal_recall_payload(
        context=context,
        nearest_player=nearest_player,
        config=config,
        net_axis_reversal=net_axis_reversal or {},
    )
    recall_payload["diagnostic_only"] = True
    return EventCandidateRejectionDiagnostic(
        trajectory_context=context,
        nearest_player=nearest_player,
        net_axis_reversal=net_axis_reversal or {},
        vertical_motion_proxy={},
        speed_reduction={},
        inside_or_near_court_template=_inside_or_near_template(
            anchor,
            config.bounce_inside_template_margin,
        ),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.hit_player_review_distance_max_template,
            away_from_player=False,
        ),
        candidate_decision={
            "selected_candidate_type": None,
            "reason": "net_axis_reversal_hit_recall_rejected",
            "rejection_reasons": rejection_reasons,
            "classification_priority": "net_axis_reversal_hit_recall_then_sequence_prior",
            "diagnostic_source": "net_axis_reversal_hit_recall",
            "player_proximity_required": False,
        },
        rejection_reasons=rejection_reasons,
        diagnostic_source="net_axis_reversal_hit_recall",
        net_axis_reversal_recall=recall_payload,
    )


def _synthetic_player_anchor_point(player: PlayerProjection) -> TrajectoryPoint:
    return TrajectoryPoint(
        trajectory_observation=player.observation,
        frame_number=player.frame_number,
        timestamp_ms=player.timestamp_ms,
        court_x=player.court_x,
        court_y=player.court_y,
        source_ball_court_projection_observation_id=None,
        source_homography_observation_id=None,
        homography_time_delta_ms=None,
        homography_carried_forward=False,
        inside_template_bounds=0.0 <= player.court_x <= 1.0
        and 0.0 <= player.court_y <= 1.0,
    )


def _synthetic_neighbor_point(
    point: TrajectoryPoint,
    *,
    timestamp_ms: int,
    frame_number: int,
) -> TrajectoryPoint:
    return TrajectoryPoint(
        trajectory_observation=point.trajectory_observation,
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        court_x=point.court_x,
        court_y=point.court_y,
        source_ball_court_projection_observation_id=(
            point.source_ball_court_projection_observation_id
        ),
        source_homography_observation_id=point.source_homography_observation_id,
        homography_time_delta_ms=point.homography_time_delta_ms,
        homography_carried_forward=point.homography_carried_forward,
        inside_template_bounds=point.inside_template_bounds,
        image_x=point.image_x,
        image_y=point.image_y,
    )


def _rejection_diagnostic_from_candidate(
    candidate: EventCandidateDraft,
    *,
    rejection_reasons: list[str],
    decision_reason: str,
    suppressed_by_observation_type: str | None = None,
    suppressed_by_frame: int | None = None,
    suppressed_by_timestamp_ms: int | None = None,
    overlap_suppression: dict[str, Any] | None = None,
) -> EventCandidateRejectionDiagnostic:
    candidate_decision = {
        "selected_candidate_type": None,
        "attempted_candidate_type": candidate.observation_type,
        "reason": decision_reason,
        "rejection_reasons": rejection_reasons,
        "classification_priority": "side_zone_sequence_candidate_prior",
    }
    if suppressed_by_observation_type is not None:
        candidate_decision["suppressed_by_observation_type"] = (
            suppressed_by_observation_type
        )
        candidate_decision["suppressed_by_frame"] = suppressed_by_frame
        candidate_decision["suppressed_by_timestamp_ms"] = suppressed_by_timestamp_ms
    return EventCandidateRejectionDiagnostic(
        trajectory_context=candidate.trajectory_context,
        nearest_player=candidate.nearest_player,
        net_axis_reversal=candidate.net_axis_reversal or {},
        vertical_motion_proxy=candidate.vertical_motion_proxy or {},
        speed_reduction=candidate.speed_reduction or {},
        player_proximity_gate=candidate.player_proximity_gate,
        candidate_decision=candidate_decision,
        rejection_reasons=rejection_reasons,
        inside_or_near_court_template=_inside_or_near_template(
            candidate.trajectory_context.current,
            DEFAULT_BOUNCE_TEMPLATE_MARGIN,
        ),
        diagnostic_source=(
            "player_anchored_hit_recall"
            if candidate.candidate_method == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
            else "net_axis_reversal_hit_recall"
            if candidate.candidate_method == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
            else "local_trajectory_context"
        ),
        player_anchored_hit_recall=candidate.player_anchored_hit_recall,
        player_anchor_contact_zone=candidate.player_anchor_contact_zone,
        net_axis_reversal_recall=candidate.net_axis_reversal_recall,
        overlap_suppression=overlap_suppression or candidate.overlap_suppression,
    )


def _rejection_reason_counts(
    diagnostics: list[EventCandidateRejectionDiagnostic],
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for diagnostic in diagnostics:
        counts.update(diagnostic.rejection_reasons)
    return dict(sorted(counts.items()))


def _persist_event_candidates_and_diagnostics(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    candidates: list[EventCandidateDraft],
    diagnostics: list[EventCandidateRejectionDiagnostic],
) -> list[Any]:
    observations = _persist_event_candidates(
        writer=writer,
        media=media,
        run=run,
        step=step,
        model=model,
        runtime_config=runtime_config,
        ball_trajectory_run_id=ball_trajectory_run_id,
        court_projection_run_id=court_projection_run_id,
        candidates=candidates,
    )
    observations.extend(
        _persist_event_candidate_diagnostics(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            diagnostics=diagnostics,
        )
    )
    return observations


def _persist_event_candidates(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    candidates: list[EventCandidateDraft],
) -> list[Any]:
    observations = []
    for index, candidate in enumerate(candidates):
        observations.append(
            writer.write(
                _event_candidate_observation_create(
                    media=media,
                    run=run,
                    step=step,
                    model=model,
                    runtime_config=runtime_config,
                    ball_trajectory_run_id=ball_trajectory_run_id,
                    court_projection_run_id=court_projection_run_id,
                    candidate=candidate,
                    index=index,
                )
            )
        )
    return observations


def _persist_event_candidate_diagnostics(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    diagnostics: list[EventCandidateRejectionDiagnostic],
) -> list[Any]:
    observations = []
    for index, diagnostic in enumerate(diagnostics):
        observations.append(
            writer.write(
                _event_candidate_diagnostic_observation_create(
                    media=media,
                    run=run,
                    step=step,
                    model=model,
                    runtime_config=runtime_config,
                    ball_trajectory_run_id=ball_trajectory_run_id,
                    court_projection_run_id=court_projection_run_id,
                    diagnostic=diagnostic,
                    index=index,
                )
            )
        )
    return observations


def _event_candidate_observation_create(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    candidate: EventCandidateDraft,
    index: int,
) -> ObservationCreate:
    current = candidate.trajectory_context.current
    is_hit = candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
    payload = {
        "candidate_type": candidate.observation_type,
        "source_ball_trajectory_run_id": ball_trajectory_run_id,
        "source_ball_trajectory_observation_id": current.trajectory_observation.id,
        "source_court_projection_run_id": court_projection_run_id,
        "source_ball_court_projection_observation_id": (
            current.source_ball_court_projection_observation_id
        ),
        "frame_number": current.frame_number,
        "timestamp_ms": current.timestamp_ms,
        "court_point": {"x": _round(current.court_x), "y": _round(current.court_y)},
        "trajectory_context": _trajectory_context_payload(candidate.trajectory_context),
        "reason_codes": candidate.reason_codes,
        "confidence": candidate.confidence,
        "candidate_method": candidate.candidate_method,
        "classification_priority": "side_zone_sequence_candidate_prior",
        "player_proximity_gate": candidate.player_proximity_gate,
        "candidate_decision": candidate.candidate_decision,
        "coordinate_space": CoordinateSpace.court_template_2d,
        "template_name": COURT_TEMPLATE_NAME,
        "template_version": COURT_TEMPLATE_VERSION,
        "source_label": (
            "hit candidate evidence" if is_hit else "bounce candidate evidence"
        ),
        "evidence_source": "event_candidate",
        "not_ball_truth": True,
        **EVENT_CANDIDATE_WARNINGS,
    }
    if candidate.nearest_player is not None:
        payload["nearest_player"] = _nearest_player_payload(candidate.nearest_player)
        payload["source_player_court_projection_observation_id"] = (
            candidate.nearest_player.player.observation.id
        )
    else:
        payload["nearest_player"] = None
        payload["source_player_court_projection_observation_id"] = None
    if candidate.net_axis_reversal is not None:
        payload["net_axis_reversal"] = candidate.net_axis_reversal
    if candidate.vertical_motion_proxy is not None:
        payload["vertical_motion_proxy"] = candidate.vertical_motion_proxy
    if candidate.speed_reduction is not None:
        payload["speed_reduction"] = candidate.speed_reduction
    if candidate.court_side_zone is not None:
        payload["court_side_zone"] = candidate.court_side_zone
    if candidate.player_contact_zone is not None:
        payload["player_contact_zone"] = candidate.player_contact_zone
    if candidate.court_landing_zone is not None:
        payload["court_landing_zone"] = candidate.court_landing_zone
    if candidate.candidate_reclassification is not None:
        payload["candidate_reclassification"] = candidate.candidate_reclassification
    if candidate.candidate_sequence is not None:
        payload["candidate_sequence"] = candidate.candidate_sequence
    if candidate.player_anchored_hit_recall is not None:
        payload["player_anchored_hit_recall"] = candidate.player_anchored_hit_recall
    if candidate.player_anchor_contact_zone is not None:
        payload["player_anchor_contact_zone"] = candidate.player_anchor_contact_zone
    if candidate.net_axis_reversal_recall is not None:
        payload["net_axis_reversal_recall"] = candidate.net_axis_reversal_recall
    if candidate.overlap_suppression is not None:
        payload["overlap_suppression"] = candidate.overlap_suppression
    if candidate.original_observation_type is not None:
        payload["original_candidate_type"] = candidate.original_observation_type
    if candidate.original_candidate_method is not None:
        payload["original_candidate_method"] = candidate.original_candidate_method
    lineage = [
        ObservationLineageCreate(
            parent_observation_id=current.trajectory_observation.id,
            relationship_type=RelationshipType.candidate_from_ball_trajectory,
            processing_step_id=step.id,
            payload_jsonb={
                "candidate_type": candidate.observation_type,
                "candidate_method": candidate.candidate_method,
                **EVENT_CANDIDATE_WARNINGS,
            },
        )
    ]
    if current.source_ball_court_projection_observation_id is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=current.source_ball_court_projection_observation_id,
                relationship_type=RelationshipType.candidate_from_ball_court_projection,
                processing_step_id=step.id,
                payload_jsonb={
                    "candidate_type": candidate.observation_type,
                    "candidate_method": candidate.candidate_method,
                    **EVENT_CANDIDATE_WARNINGS,
                },
            )
        )
    if candidate.nearest_player is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=candidate.nearest_player.player.observation.id,
                relationship_type=RelationshipType.candidate_from_main_player_court_projection,
                processing_step_id=step.id,
                payload_jsonb={
                    "candidate_type": candidate.observation_type,
                    "candidate_method": candidate.candidate_method,
                    **EVENT_CANDIDATE_WARNINGS,
                },
            )
        )
    return ObservationCreate(
        media_id=media.id,
        run_id=run.id,
        observation_family=ObservationFamily.event_candidate,
        observation_type=candidate.observation_type,
        granularity=ObservationGranularity.frame,
        frame_start=current.frame_number,
        frame_end=current.frame_number,
        timestamp_start_ms=current.timestamp_ms,
        timestamp_end_ms=current.timestamp_ms,
        confidence=candidate.confidence,
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space=CoordinateSpace.court_template_2d,
        payload_jsonb={
            **payload,
            "processing_step_id": step.id,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
        },
        idempotency_key=(
            f"{run.id}:{candidate.observation_type}:"
            f"{current.trajectory_observation.id}:{current.frame_number}:{index}"
        ),
        lineage=lineage,
    )


def _event_candidate_diagnostic_observation_create(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    diagnostic: EventCandidateRejectionDiagnostic,
    index: int,
) -> ObservationCreate:
    current = diagnostic.trajectory_context.current
    payload = {
        "candidate_type": EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE,
        "source_ball_trajectory_run_id": ball_trajectory_run_id,
        "source_ball_trajectory_observation_id": current.trajectory_observation.id,
        "source_court_projection_run_id": court_projection_run_id,
        "source_ball_court_projection_observation_id": (
            current.source_ball_court_projection_observation_id
        ),
        "frame_number": current.frame_number,
        "timestamp_ms": current.timestamp_ms,
        "court_point": {"x": _round(current.court_x), "y": _round(current.court_y)},
        "image_point": (
            {"x": _round(current.image_x), "y": _round(current.image_y)}
            if current.image_x is not None and current.image_y is not None
            else None
        ),
        "trajectory_context": _trajectory_context_payload(diagnostic.trajectory_context),
        "net_axis_reversal": diagnostic.net_axis_reversal,
        "vertical_motion_proxy": diagnostic.vertical_motion_proxy,
        "speed_reduction": diagnostic.speed_reduction,
        "player_proximity_gate": diagnostic.player_proximity_gate,
        "candidate_decision": diagnostic.candidate_decision,
        "rejection_reasons": diagnostic.rejection_reasons,
        "inside_or_near_court_template": diagnostic.inside_or_near_court_template,
        "diagnostic_source": diagnostic.diagnostic_source,
        "diagnostic_only": True,
        "candidate_method": EVENT_CANDIDATE_METHOD,
        "classification_priority": "player_anchored_hit_recall_then_sequence_prior",
        "coordinate_space": CoordinateSpace.court_template_2d,
        "template_name": COURT_TEMPLATE_NAME,
        "template_version": COURT_TEMPLATE_VERSION,
            "source_label": "hit/bounce candidate rejection diagnostic",
        "evidence_source": "event_candidate_diagnostic",
        "not_ball_truth": True,
        **EVENT_CANDIDATE_WARNINGS,
    }
    if diagnostic.nearest_player is not None:
        payload["nearest_player"] = _nearest_player_payload(diagnostic.nearest_player)
        payload["source_player_court_projection_observation_id"] = (
            diagnostic.nearest_player.player.observation.id
        )
    else:
        payload["nearest_player"] = None
        payload["source_player_court_projection_observation_id"] = None
    if diagnostic.player_anchored_hit_recall is not None:
        payload["player_anchored_hit_recall"] = diagnostic.player_anchored_hit_recall
    if diagnostic.player_anchor_contact_zone is not None:
        payload["player_anchor_contact_zone"] = diagnostic.player_anchor_contact_zone
    if diagnostic.net_axis_reversal_recall is not None:
        payload["net_axis_reversal_recall"] = diagnostic.net_axis_reversal_recall
    if diagnostic.overlap_suppression is not None:
        payload["overlap_suppression"] = diagnostic.overlap_suppression
    lineage = [
        ObservationLineageCreate(
            parent_observation_id=current.trajectory_observation.id,
            relationship_type=RelationshipType.derived_from,
            processing_step_id=step.id,
            payload_jsonb={
                "candidate_type": EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE,
                "candidate_method": EVENT_CANDIDATE_METHOD,
                "diagnostic_only": True,
                **EVENT_CANDIDATE_WARNINGS,
            },
        )
    ]
    if current.source_ball_court_projection_observation_id is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=current.source_ball_court_projection_observation_id,
                relationship_type=RelationshipType.derived_from,
                processing_step_id=step.id,
                payload_jsonb={
                    "candidate_type": (
                        EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE
                    ),
                    "candidate_method": EVENT_CANDIDATE_METHOD,
                    "diagnostic_only": True,
                    **EVENT_CANDIDATE_WARNINGS,
                },
            )
        )
    if diagnostic.nearest_player is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=diagnostic.nearest_player.player.observation.id,
                relationship_type=RelationshipType.derived_from,
                processing_step_id=step.id,
                payload_jsonb={
                    "candidate_type": (
                        EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE
                    ),
                    "candidate_method": EVENT_CANDIDATE_METHOD,
                    "diagnostic_only": True,
                    **EVENT_CANDIDATE_WARNINGS,
                },
            )
        )
    return ObservationCreate(
        media_id=media.id,
        run_id=run.id,
        observation_family=ObservationFamily.event_candidate,
        observation_type=EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE,
        granularity=ObservationGranularity.frame,
        frame_start=current.frame_number,
        frame_end=current.frame_number,
        timestamp_start_ms=current.timestamp_ms,
        timestamp_end_ms=current.timestamp_ms,
        confidence=None,
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space=CoordinateSpace.court_template_2d,
        payload_jsonb={
            **payload,
            "processing_step_id": step.id,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
        },
        idempotency_key=(
            f"{run.id}:{EVENT_CANDIDATE_REJECTION_DIAGNOSTIC_OBSERVATION_TYPE}:"
            f"{current.trajectory_observation.id}:{current.frame_number}:{index}"
        ),
        lineage=lineage,
    )


def _trajectory_points_from_observation(
    row: Observation,
    *,
    image_points_by_observation_id: dict[str, tuple[float, float]] | None = None,
) -> list[TrajectoryPoint]:
    payload = row.payload_jsonb or {}
    raw_points = payload.get("points")
    if not isinstance(raw_points, list):
        return []
    image_points_by_observation_id = image_points_by_observation_id or {}
    points = []
    for raw_point in raw_points:
        if not isinstance(raw_point, dict):
            continue
        frame_number = _optional_int(raw_point.get("frame_number"))
        timestamp_ms = _optional_int(raw_point.get("timestamp_ms"))
        court_x = _number(raw_point.get("court_x"))
        court_y = _number(raw_point.get("court_y"))
        if frame_number is None or timestamp_ms is None or court_x is None or court_y is None:
            continue
        source_ball_court_projection_observation_id = _string_or_none(
            raw_point.get("source_observation_id")
            or raw_point.get("source_ball_court_projection_observation_id")
        )
        image_point = (
            image_points_by_observation_id.get(
                source_ball_court_projection_observation_id or ""
            )
            or _image_point_tuple(raw_point.get("image_point"))
        )
        points.append(
            TrajectoryPoint(
                trajectory_observation=row,
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                court_x=court_x,
                court_y=court_y,
                source_ball_court_projection_observation_id=(
                    source_ball_court_projection_observation_id
                ),
                source_homography_observation_id=_string_or_none(
                    raw_point.get("source_homography_observation_id")
                ),
                homography_time_delta_ms=_optional_int(
                    raw_point.get("homography_time_delta_ms")
                ),
                homography_carried_forward=bool(
                    raw_point.get("homography_carried_forward")
                ),
                inside_template_bounds=bool(
                    raw_point.get(
                        "inside_template_bounds",
                        0.0 <= court_x <= 1.0 and 0.0 <= court_y <= 1.0,
                    )
                ),
                image_x=image_point[0] if image_point is not None else None,
                image_y=image_point[1] if image_point is not None else None,
            )
        )
    return sorted(points, key=lambda point: (point.timestamp_ms, point.frame_number))


def _player_projection_from_observation(row: Observation) -> PlayerProjection | None:
    payload = row.payload_jsonb or {}
    court_point = payload.get("court_point")
    image_anchor = payload.get("image_anchor")
    frame_number = _optional_int(row.frame_start)
    if frame_number is None:
        frame_number = _optional_int(payload.get("frame_number"))
    timestamp_ms = _optional_int(row.timestamp_start_ms)
    if timestamp_ms is None:
        timestamp_ms = _optional_int(payload.get("timestamp_ms"))
    if not isinstance(court_point, dict) or frame_number is None or timestamp_ms is None:
        return None
    court_x = _number(court_point.get("x"))
    court_y = _number(court_point.get("y"))
    if court_x is None or court_y is None:
        return None
    return PlayerProjection(
        observation=row,
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        court_x=court_x,
        court_y=court_y,
        track_candidate_id=_string_or_none(payload.get("track_candidate_id")),
        track_role_candidate=_string_or_none(payload.get("track_role_candidate")),
        image_x=(
            _number(image_anchor.get("x")) if isinstance(image_anchor, dict) else None
        ),
        image_y=(
            _number(image_anchor.get("y")) if isinstance(image_anchor, dict) else None
        ),
    )


def _trajectory_context_payload(context: TrajectoryContext) -> dict[str, Any]:
    return {
        "previous_frame": context.previous.frame_number,
        "next_frame": context.next.frame_number,
        "previous_timestamp_ms": context.previous.timestamp_ms,
        "next_timestamp_ms": context.next.timestamp_ms,
        "direction_before_degrees": context.direction_before_degrees,
        "direction_after_degrees": context.direction_after_degrees,
        "direction_delta_degrees": context.direction_delta_degrees,
        "speed_before": context.speed_before,
        "speed_after": context.speed_after,
        "speed_delta_fraction": context.speed_delta_fraction,
    }


def _nearest_player_payload(nearest_player: NearestPlayerContext) -> dict[str, Any]:
    player = nearest_player.player
    return {
        "track_role_candidate": player.track_role_candidate,
        "track_candidate_id": player.track_candidate_id,
        "source_player_court_projection_observation_id": player.observation.id,
        "court_x": _round(player.court_x),
        "court_y": _round(player.court_y),
        "distance_template_units": nearest_player.distance_template_units,
        "time_delta_ms": nearest_player.time_delta_ms,
    }


def _player_proximity_gate_payload(
    *,
    nearest_player: NearestPlayerContext | None,
    threshold: float,
    away_from_player: bool,
) -> dict[str, Any]:
    if nearest_player is None:
        return {
            "nearest_player_found": False,
            "distance_template_units": None,
            "time_delta_ms": None,
            "threshold": threshold,
            "away_from_player": away_from_player,
        }
    return {
        "nearest_player_found": True,
        "distance_template_units": nearest_player.distance_template_units,
        "time_delta_ms": nearest_player.time_delta_ms,
        "threshold": threshold,
        "away_from_player": away_from_player,
    }


def _dedupe_key(candidate: EventCandidateDraft) -> str:
    if candidate.observation_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE:
        return candidate.observation_type
    role = (
        candidate.nearest_player.player.track_role_candidate
        if candidate.nearest_player is not None
        else None
    )
    return f"{candidate.observation_type}:{role or 'unknown'}"


def _inside_or_near_template(point: TrajectoryPoint, margin: float) -> bool:
    return (
        -margin <= point.court_x <= 1.0 + margin
        and -margin <= point.court_y <= 1.0 + margin
    )


def _image_point_tuple(value: Any) -> tuple[float, float] | None:
    if not isinstance(value, dict):
        return None
    x = _number(value.get("x"))
    y = _number(value.get("y"))
    if x is None or y is None:
        return None
    return (x, y)


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "hit-bounce-candidate-evidence",
            ModelRegistry.version == "v0.2.4",
            ModelRegistry.model_family == "event_candidate",
            ModelRegistry.source == "apps.worker.services.hit_bounce_candidates",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="hit-bounce-candidate-evidence",
        version="v0.2.4",
        model_family="event_candidate",
        source="apps.worker.services.hit_bounce_candidates",
        metadata_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            "hit_candidate_method": HIT_CANDIDATE_METHOD,
            "player_anchored_hit_candidate_method": PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
            "bounce_candidate_method": BOUNCE_CANDIDATE_METHOD,
            **EVENT_CANDIDATE_WARNINGS,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    config: HitBounceCandidateConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="hit-bounce-candidate-evidence-config",
        config_version="v0.2.4",
        payload_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            "source_ball_trajectory_run_id": ball_trajectory_run_id,
            "source_court_projection_run_id": court_projection_run_id,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "coordinate_space": CoordinateSpace.court_template_2d,
            **config.as_dict(),
            **EVENT_CANDIDATE_WARNINGS,
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _create_run(
    *,
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    config: HitBounceCandidateConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            "source_ball_trajectory_run_id": ball_trajectory_run_id,
            "source_court_projection_run_id": court_projection_run_id,
            "evidence_source": "event_candidate",
            "source_label": "hit/bounce candidate evidence",
            **config.as_dict(),
            **EVENT_CANDIDATE_WARNINGS,
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    *,
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="player_anchored_hit_contact_zone_tightening_v024",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            **EVENT_CANDIDATE_WARNINGS,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_counts: dict[str, int],
    output_counts: dict[str, int],
    candidate_summary: dict[str, Any],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "candidate_method": EVENT_CANDIDATE_METHOD,
        "source_counts": source_counts,
        "output_counts": output_counts,
        "candidate_summary": candidate_summary,
        "hit_candidate_count": output_counts.get(HIT_CANDIDATE_OBSERVATION_TYPE, 0),
        "bounce_candidate_count": output_counts.get(BOUNCE_CANDIDATE_OBSERVATION_TYPE, 0),
        **EVENT_CANDIDATE_WARNINGS,
    }
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {**(run.metadata_jsonb or {}), **summary}
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {**(step.metadata_jsonb or {}), **summary}
    session.commit()


def _mark_failed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        "error": message,
        **EVENT_CANDIDATE_WARNINGS,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        **EVENT_CANDIDATE_WARNINGS,
    }
    session.commit()


def _validate_config(config: HitBounceCandidateConfig) -> dict[str, Any] | None:
    if config.hit_player_distance_max_template <= 0:
        return _failed(
            "invalid_hit_player_distance_max_template",
            "hit_player_distance_max_template must be greater than zero",
        )
    if config.hit_player_review_distance_max_template < config.hit_player_distance_max_template:
        return _failed(
            "invalid_hit_player_review_distance_max_template",
            "hit_player_review_distance_max_template must be greater than or equal to "
            "hit_player_distance_max_template",
        )
    if config.hit_near_player_direction_delta_degrees < 0:
        return _failed(
            "invalid_hit_near_player_direction_delta_degrees",
            "hit_near_player_direction_delta_degrees must be greater than or equal to zero",
        )
    if config.hit_min_net_axis_delta_template <= 0:
        return _failed(
            "invalid_hit_min_net_axis_delta_template",
            "hit_min_net_axis_delta_template must be greater than zero",
        )
    if config.hit_min_speed_delta_fraction < 0:
        return _failed(
            "invalid_hit_min_speed_delta_fraction",
            "hit_min_speed_delta_fraction must be greater than or equal to zero",
        )
    if config.hit_contact_fallback_min_speed_delta_fraction < 0:
        return _failed(
            "invalid_hit_contact_fallback_min_speed_delta_fraction",
            "hit_contact_fallback_min_speed_delta_fraction must be greater than or equal to zero",
        )
    if config.hit_contact_fallback_min_direction_delta_degrees < 0:
        return _failed(
            "invalid_hit_contact_fallback_min_direction_delta_degrees",
            "hit_contact_fallback_min_direction_delta_degrees must be greater than "
            "or equal to zero",
        )
    if config.bounce_player_distance_min_template < 0:
        return _failed(
            "invalid_bounce_player_distance_min_template",
            "bounce_player_distance_min_template must be greater than or equal to zero",
        )
    if config.hit_min_direction_delta_degrees < 0:
        return _failed(
            "invalid_hit_min_direction_delta_degrees",
            "hit_min_direction_delta_degrees must be greater than or equal to zero",
        )
    if config.bounce_min_direction_delta_degrees < 0:
        return _failed(
            "invalid_bounce_min_direction_delta_degrees",
            "bounce_min_direction_delta_degrees must be greater than or equal to zero",
        )
    if config.bounce_min_image_y_delta_pixels <= 0:
        return _failed(
            "invalid_bounce_min_image_y_delta_pixels",
            "bounce_min_image_y_delta_pixels must be greater than zero",
        )
    if config.bounce_min_speed_reduction_fraction < 0:
        return _failed(
            "invalid_bounce_min_speed_reduction_fraction",
            "bounce_min_speed_reduction_fraction must be greater than or equal to zero",
        )
    if config.bounce_fallback_min_speed_reduction_fraction < 0:
        return _failed(
            "invalid_bounce_fallback_min_speed_reduction_fraction",
            "bounce_fallback_min_speed_reduction_fraction must be greater than or equal to zero",
        )
    if config.candidate_dedupe_ms < 0:
        return _failed(
            "invalid_candidate_dedupe_ms",
            "candidate_dedupe_ms must be greater than or equal to zero",
        )
    if config.player_time_window_ms < 0:
        return _failed(
            "invalid_player_time_window_ms",
            "player_time_window_ms must be greater than or equal to zero",
        )
    if config.player_anchored_hit_lookback_ms <= 0:
        return _failed(
            "invalid_player_anchored_hit_lookback_ms",
            "player_anchored_hit_lookback_ms must be greater than zero",
        )
    if config.player_anchored_hit_lookahead_ms <= 0:
        return _failed(
            "invalid_player_anchored_hit_lookahead_ms",
            "player_anchored_hit_lookahead_ms must be greater than zero",
        )
    if config.player_anchored_hit_distance_max_template <= 0:
        return _failed(
            "invalid_player_anchored_hit_distance_max_template",
            "player_anchored_hit_distance_max_template must be greater than zero",
        )
    if config.player_anchored_hit_min_net_axis_delta_template <= 0:
        return _failed(
            "invalid_player_anchored_hit_min_net_axis_delta_template",
            "player_anchored_hit_min_net_axis_delta_template must be greater than zero",
        )
    if config.player_anchored_hit_min_pre_post_gap_ms < 0:
        return _failed(
            "invalid_player_anchored_hit_min_pre_post_gap_ms",
            "player_anchored_hit_min_pre_post_gap_ms must be greater than or equal to zero",
        )
    if config.event_overlap_distance_template <= 0:
        return _failed(
            "invalid_event_overlap_distance_template",
            "event_overlap_distance_template must be greater than zero",
        )
    if config.net_axis_reversal_lookback_ms <= 0:
        return _failed(
            "invalid_net_axis_reversal_lookback_ms",
            "net_axis_reversal_lookback_ms must be greater than zero",
        )
    if config.net_axis_reversal_lookahead_ms <= 0:
        return _failed(
            "invalid_net_axis_reversal_lookahead_ms",
            "net_axis_reversal_lookahead_ms must be greater than zero",
        )
    if config.net_axis_reversal_min_delta_template <= 0:
        return _failed(
            "invalid_net_axis_reversal_min_delta_template",
            "net_axis_reversal_min_delta_template must be greater than zero",
        )
    if config.net_axis_reversal_min_pre_post_gap_ms < 0:
        return _failed(
            "invalid_net_axis_reversal_min_pre_post_gap_ms",
            "net_axis_reversal_min_pre_post_gap_ms must be greater than or equal to zero",
        )
    if config.net_axis_reversal_dedupe_distance_template <= 0:
        return _failed(
            "invalid_net_axis_reversal_dedupe_distance_template",
            "net_axis_reversal_dedupe_distance_template must be greater than zero",
        )
    return None


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(EVENT_CANDIDATE_WARNINGS),
        **extra,
    }


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        number = float(value)
        return number if math.isfinite(number) else None
    return None


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return int(value)
    return None


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _round(value: float, digits: int = 6) -> float:
    return round(float(value), digits)
