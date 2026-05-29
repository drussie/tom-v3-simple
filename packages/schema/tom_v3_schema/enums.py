from enum import StrEnum


class MediaType(StrEnum):
    video = "video"


class RunStatus(StrEnum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    partial = "partial"


class StepStatus(StrEnum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    partial = "partial"


class ModelFamily(StrEnum):
    detection = "detection"
    gameplay = "gameplay"
    ball = "ball"
    player = "player"
    pose = "pose"
    court = "court"
    homography = "homography"
    tracker = "tracker"
    derived = "derived"
    synthetic = "synthetic"


class ObservationFamily(StrEnum):
    gameplay = "gameplay"
    atomic = "atomic"
    derived = "derived"
    pose = "pose"
    court = "court"
    homography = "homography"
    tracking = "tracking"
    artifact = "artifact"


class ObservationGranularity(StrEnum):
    frame = "frame"
    frame_range = "frame_range"
    track_point = "track_point"
    tracklet = "tracklet"
    segment = "segment"
    video = "video"
    run = "run"


class ViewState(StrEnum):
    gameplay = "gameplay"
    non_gameplay = "non_gameplay"
    uncertain = "uncertain"


class ViewStateSubtype(StrEnum):
    active_point = "active_point"
    between_points = "between_points"
    serve_setup = "serve_setup"
    changeover = "changeover"
    replay = "replay"
    scoreboard = "scoreboard"
    camera_cut = "camera_cut"
    closeup = "closeup"
    crowd_shot = "crowd_shot"
    broadcast_graphic = "broadcast_graphic"
    unknown = "unknown"


class AtomicKind(StrEnum):
    ball_detection = "ball_detection"
    player_detection = "player_detection"
    pose_keypoints = "pose_keypoints"
    court_line = "court_line"
    court_corner = "court_corner"


class DerivedKind(StrEnum):
    bounce_candidate = "bounce_candidate"
    hit_candidate = "hit_candidate"
    trajectory_segment = "trajectory_segment"
    tracking_gap_candidate = "tracking_gap_candidate"


class RelationshipType(StrEnum):
    derived_from = "derived_from"
    tracked_from = "tracked_from"
    grouped_from = "grouped_from"
    scoped_by = "scoped_by"
    projected_using = "projected_using"
    rendered_from = "rendered_from"
    grouped_with = "grouped_with"
    pose_from_subject_detection_candidate = "pose_from_subject_detection_candidate"
    main_subject_candidate_from_player_detection = (
        "main_subject_candidate_from_player_detection"
    )
    main_player_track_assignment_from_subject_candidate = (
        "main_player_track_assignment_from_subject_candidate"
    )
    main_player_track_assignment_from_player_detection = (
        "main_player_track_assignment_from_player_detection"
    )
    main_player_track_assignment_for_track_candidate = (
        "main_player_track_assignment_for_track_candidate"
    )
    pose_from_main_subject_candidate = "pose_from_main_subject_candidate"
    pose_from_main_player_track_assignment = "pose_from_main_player_track_assignment"
    pose_from_main_player_track_candidate = "pose_from_main_player_track_candidate"
    subject_context_candidate = "subject_context_candidate"
    pose_from_track_point_candidate = "pose_from_track_point_candidate"
    homography_from_court_keypoints_candidate = "homography_from_court_keypoints_candidate"
    homography_from_court_lines_candidate = "homography_from_court_lines_candidate"
    camera_context_for_homography_candidate = "camera_context_for_homography_candidate"
    projection_diagnostic_for_homography_candidate = (
        "projection_diagnostic_for_homography_candidate"
    )
    smoothed_from_ball_detection = "smoothed_from_ball_detection"
    smoothed_from_track_point_candidate = "smoothed_from_track_point_candidate"
    smoothed_from_main_player_track_assignment = (
        "smoothed_from_main_player_track_assignment"
    )
    smoothed_from_pose_observation = "smoothed_from_pose_observation"


class CoordinateSpace(StrEnum):
    image_pixels = "image_pixels"
    normalized_frame = "normalized_frame"
    court_template_2d = "court_template_2d"
    court_plane = "court_plane"
    world_estimate = "world_estimate"
    none = "none"
